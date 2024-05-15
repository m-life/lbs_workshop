from service import get_client
from config import get_settings
from lib.text_utils import (
    start_job,
    get_job_response,
    get_job_results,
    get_text_with_info,
    get_text_with_line_spacing_info,
    extract_paragraphs_only,
    get_paragraphs_based_on_period
)

settings = get_settings()
textract = get_client('textract', settings)

jid = start_job(textract, settings.bucket_name, 'interpretation_light.pdf')
row_response = get_job_response(textract, jid)
result = get_job_results(textract, jid)
result_info = get_text_with_info(result)
result_info_completed = get_text_with_line_spacing_info(result_info)
test_paragraph = extract_paragraphs_only(result_info_completed)
paragraphs = get_paragraphs_based_on_period(result_info_completed)
