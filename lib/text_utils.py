import time


def start_job(client, bucket_name, object_name):
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def get_job_response(client, job_id):
    response = None
    status = 'IN_PROGRESS'
    while status == "IN_PROGRESS":
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return response


def get_job_results(client, job_id):
    pages = []
    next_token = None
    params = {'JobId': job_id}

    while next_token or len(pages) == 0:
        time.sleep(1)
        if next_token is not None:
            params['NextToken'] = next_token
        response = client.get_document_text_detection(**params)
        pages.append(response)
        print(f"Page received: {len(pages)}")
        next_token = response['NextToken'] if 'NextToken' in response else None

    return pages


def get_text_with_info(page_collections):
    total_text = []
    total_text_with_info = []
    running_sequence_number = 0

    font_sizes_and_line_numbers = {}
    for page in page_collections:
        per_page_text = []
        for block in page['Blocks']:
            if block['BlockType'] == 'LINE':
                block_text_dict = {}
                running_sequence_number += 1
                block_text_dict.update(text=block['Text'])
                block_text_dict.update(page=block['Page'])
                block_text_dict.update(left_indent=round(block['Geometry']['BoundingBox']['Left'], 2))
                font_height = round(block['Geometry']['BoundingBox']['Height'], 3)
                line_number = running_sequence_number
                block_text_dict.update(font_height=round(block['Geometry']['BoundingBox']['Height'], 3))
                block_text_dict.update(indent_from_top=round(block['Geometry']['BoundingBox']['Top'], 2))
                block_text_dict.update(text_width=round(block['Geometry']['BoundingBox']['Width'], 2))
                block_text_dict.update(line_number=running_sequence_number)

                if font_height in font_sizes_and_line_numbers:
                    line_numbers = font_sizes_and_line_numbers[font_height]
                    line_numbers.append(line_number)
                    font_sizes_and_line_numbers[font_height] = line_numbers
                else:
                    line_numbers = [line_number]
                    font_sizes_and_line_numbers[font_height] = line_numbers

                total_text.append(block['Text'])
                per_page_text.append(block['Text'])
                total_text_with_info.append(block_text_dict)

    return total_text_with_info


def get_text_with_line_spacing_info(text_with_info):
    i = 1
    text_info_with_line_spacing = []
    while i < len(text_with_info) - 1:
        previous_line = text_with_info[i - 1]
        current_line = text_with_info[i]
        next_line_info = text_with_info[i + 1]
        if current_line['page'] == next_line_info['page'] and previous_line['page'] == current_line['page']:
            line_spacing_after = round((next_line_info['indent_from_top'] - current_line['indent_from_top']), 2)
            spacing_with_prev = round((current_line['indent_from_top'] - previous_line['indent_from_top']), 2)
            current_line.update(line_space_before=spacing_with_prev)
            current_line.update(line_space_after=line_spacing_after)
            text_info_with_line_spacing.append(current_line)
        else:
            text_info_with_line_spacing.append(None)
        i += 1
    return text_info_with_line_spacing


def extract_paragraphs_only(data):
    paras = []
    i = 0
    paragraph_data = []
    while i < len(data):
        line = data[i]
        if line:
            if line['line_space_before'] > line['line_space_after']:
                paras.append(''.join(paragraph_data))
                paragraph_data = [line['text']]
                if i < len(data)-1:
                    next_line = data[i + 1]
                    if next_line and line['text_width'] > next_line['text_width']/2:
                        paragraph_data.append(next_line['text'])
                        i += 1
                    else:
                        paras.append(' '.join(paragraph_data))
                        paragraph_data = []
            else:
                paragraph_data.append(line['text'])
        i += 1
    return paras


def get_paragraphs_based_on_period(data):
    paragraph_data = []
    paras = []
    i = 0
    while i < len(data):
        line = data[i]
        if line:
            if line['text'][-1] == '.':
                paragraph_data.append(line['text'])
                paras.append(' '.join(paragraph_data))
                paragraph_data = []
            else:
                paragraph_data.append(line['text'])
        i += 1
    return paras

