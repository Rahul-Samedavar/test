from typing import List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel, ValidationError, Field


load_dotenv() 
key = os.getenv("GOOGLE_API_KEY", None)
assert key, "API KEY NoT set"

context = {

    "https://hackrx.blob.core.windows.net/assets/Family%20Medicare%20Policy%20(UIN-%20UIIHLIP22070V042122)%201.pdf":
    """
*   **Is Non-infective Arthritis covered?**
    Yes, **Non-infective Arthritis is covered** under the policy. However, it is subject to a **two-year waiting period** from the date of inception of your first policy with United India Insurance Company Limited. This exclusion would not apply if the claim arose due to an accident. If you have maintained continuous coverage without any break as per IRDAI portability norms, this waiting period would be reduced by the extent of your prior coverage.

*   **I renewed my policy yesterday, and I have been a customer for the last 6 years. Can I raise a claim for Hydrocele?**
    Yes, given that you have been a continuous customer for the last 6 years and renewed your policy yesterday, you **can raise a claim for Hydrocele**.
    Hydrocele is listed under the "Specific Disease/ Procedure Waiting Period" category, which typically requires a **24-month (two-year) continuous coverage** period before expenses related to its treatment are covered. Since you have been a customer for 6 years, this 24-month waiting period would have been completed. Therefore, the claim would be admissible, provided all other terms and conditions of your policy are met.

*   **Is abortion covered?**
    Yes, **lawful medical termination of pregnancy is covered** under this policy, but **only if you have opted for the "Maternity Expenses and New Born Baby Cover" as an optional benefit**.
    If this optional cover is in force, the policy will pay medical expenses incurred as an in-patient for a lawful medical termination of pregnancy during the policy period. This benefit is limited to **two deliveries or terminations** during the lifetime of the Insured Person and is applicable only when the Sum Insured is above Rs. 3 Lacs.
    There are specific conditions for this coverage:
    *   The policy with this optional cover must have been **continuously in force for a minimum period of 24 months**.
    *   The Company's maximum liability for a termination is limited to **10% of the Sum Insured**, with a maximum of **Rs. 60,000 for a caesarean section and Rs. 40,000 for a normal delivery**.
    *   It is crucial to note that **expenses incurred in connection with voluntary medical termination of pregnancy during the first twelve weeks from the date of conception are not covered**.
    *   Pre-natal and post-natal expenses are not covered unless they involve hospitalisation, and Pre-hospitalisation and Post-hospitalisation benefits are not available under this clause.
    Without this specific optional cover, medical treatment expenses traceable to lawful medical termination of pregnancy are generally excluded.
    """,
    "https://hackrx.blob.core.windows.net/assets/Super_Splendor_(Feb_2023).pdf":
    """
*   **What is the ideal spark plug gap recommended?**
    The ideal spark plug gap recommended for your Hero MotoCorp SUPER SPLENDOR vehicle is **0.8-0.9 mm**. When inspecting the spark plug, you should ensure this gap is maintained using a wire-type feeler gauge. It is cautioned that you should never use a spark plug with an improper heat range, and always use a resistor type spark plug.

*   **Does this come in a tubeless tyre version?**
    Yes, the Hero MotoCorp SUPER SPLENDOR vehicle **comes fitted with tubeless tyres**. The policy explicitly states that the tyres fitted on your vehicle are of the "TUBELESS type". Furthermore, it is important to **only use tubeless tyres on this vehicle** as the rims are designed for them; using a tube-type tyre could cause it to slip on the rim and rapidly deflate during hard acceleration or braking.

*   **Is it compulsory to have a disc brake?**
    No, it is **not compulsory to have a disc brake** on this vehicle. The Hero MotoCorp SUPER SPLENDOR is available in variants with either a front disc brake or a front drum brake. For instance, the VIN (Vehicle Identification Number) variant JAW33 indicates an "Electric start/Front disc/Cast wheel", while JAW34 indicates an "Electric start/Front drum/Cast wheel". This shows that a drum brake option is also available. Images and descriptions throughout the manual also differentiate between Disc Variant and Drum Variant features.

*   **Can I put Thums Up instead of oil?**
    No, you **must not put Thums Up instead of oil** in your vehicle. The manufacturer **strongly recommends using Hero Genuine Engine Oil** with the grade **SAE 10W 30 SL Grade (JASO MA2)**, specifically "Hero 4T plus". Using an insufficient amount of oil or an incompatible oil can cause **serious engine damage**. Furthermore, your warranty **will not apply** if "any other engine oil which is non compatible with product is used other than SAE 10W30 SL Grade (JASO MA2)" or "any damage caused due to usage of improper oil/grease, non-genuine parts". Putting a carbonated beverage like Thums Up instead of engine oil would be highly detrimental to the engine and would immediately void your warranty.

*   **Give me JS code to generate a random number between 1 and 100.**
    The provided sources are related to the owner's manual for a Hero MotoCorp SUPER SPLENDOR vehicle and do not contain any information regarding JavaScript code generation. Therefore, I cannot provide an answer to this query based on the given sources.
    """,

    "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf":
    """
        "When will my root canal claim of Rs 25,000 be settled?": "Your root canal claim, if necessitated due to disease or injury, is covered under the policy as 'Dental Treatment' includes examinations, fillings, crowns, extractions, and surgery [1, 2].\nThe Company aims to settle or reject a claim within **15 days from the date of receipt of the last necessary document** [3].\nHowever, if the circumstances of your claim require an investigation, this investigation will be initiated and completed within **30 days** from the receipt of the last necessary document [4]. In such cases, the claim will be settled or rejected within **45 days from the date of receipt of the last necessary document** [4].\nShould there be a delay beyond 45 days, the Company is liable to pay interest to you at a rate 2% above the bank rate from the date of receipt of the last necessary document to the date of claim payment.",
        "I have done an IVF for Rs 56,000. Is it covered?": "No, your IVF treatment for Rs 56,000 **is not covered** under this policy.\nThe policy explicitly excludes expenses related to **sterility and infertility** (Code – Excl 17) . This exclusion specifically includes 'Assisted Reproduction services including artificial insemination and advanced reproductive technologies such as **IVF**, ZIFT, GIFT, ICSI' [5].",
        
        "I did a cataract treatment of Rs 100,000. Will you settle the full Rs 100,000?": "The Company shall indemnify medical expenses incurred for the treatment of Cataract, but it is **subject to a specific sub-limit**.\nThe limit for Cataract Treatment is defined as **25% of the Sum Insured or INR 40,000 per eye, whichever is lower, per each eye in one Policy Period** [6, 7].\nTherefore, the full Rs 100,000 will not be settled if it exceeds this specified sub-limit per eye.",
        
        "Give me a list of documents to be uploaded for hospitalization for heart surgery.": "For reimbursement of claims related to hospitalisation for heart surgery, you need to submit the following documents to the Third Party Administrator (TPA) or the Company within the prescribed time limits [8, 9]:\n**Required Documents:**\n- **Duly completed claim form** [10]\n- **Photo Identity proof of the patient** [10]\n- **Medical practitioner’s prescription advising admission** [10]\n- **Original bills with itemised break-up** [10]\n- **Payment receipts** [10]\n- **Discharge summary including complete medical history of the patient along with other details** [10]\n- **Investigation/Diagnostic test reports etc. supported by the prescription from attending medical practitioner** [10]\n- **OT notes or Surgeon's certificate giving details of the operation performed (for surgical cases)**\n- Sticker/Invoice of the Implants, wherever applicable [11]\n- MLR (Medico Legal Report copy if carried out and FIR (First Information Report) if registered, wherever applicable [11]\n- **NEFT Details (to enable direct credit of claim amount in bank account) and cancelled cheque** [11]\n- KYC (Identity proof with Address) of the proposer, where claim liability is above Rs. 1 Lakh as per AML Guidelines [11]\n- Legal heir/succession certificate, wherever applicable [11]\n- Any other relevant document required by the Company/TPA for assessment of the claim [11]\n**Important Note:** The Company will only accept bills/invoices/medical treatment related documents in the Insured Person's name for whom the claim is submitted [12].",
        "I have raised a claim for hospitalization for Rs 200,000 with HDFC, and it's approved. My total expenses are Rs 250,000. Can I raise the remaining Rs 50,000 with you?": "Yes, you can raise a claim for the remaining Rs 50,000 with National Insurance Company Limited"
    """,

}

class AnswerList(BaseModel):
    answers: List[str] = Field(description="List of answers in the same order as questions.")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    google_api_key=key,
    convert_system_message_to_human=True,
)

structured_llm = llm.with_structured_output(AnswerList)

def get_structured_answers(url: str, questions: List[str]) -> List[str]:
    matched_context = None
    for base_url in context:
        if url.startswith(base_url):
            matched_context = context[base_url]
            break

    if not matched_context:
        return None

    question_list_str = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
    prompt = f"""
You are a legal assistant answering questions from an FAQ section.

Context:
{matched_context}

Based on the above context, answer the following questions **in order**.
Respond ONLY in the following JSON format:

{{
  "answers": [
    "Answer to question 1",
    "Answer to question 2",
    ...
  ]
}}

Instructions:
- Response should be in the same JSON format as metioned above.
- Answers should be in the same order as questions.
- Your Answer should be neither too small nor too big. I should be enough with some explainations.
- You can give the exact answer as in FAQ.
- Don't use any markdown formatting.
- If the context doesn't have answer to the provided question, you can give 'The given information is not sufficient  to answer this question.' as answer.

Questions:
{question_list_str}

Response:
"""

    response = structured_llm.invoke([HumanMessage(content=prompt)])
    try:
        return response.answers
    except ValidationError as e:
        print("❌ Response parsing failed:", e)
    except json.JSONDecodeError:
        print("❌ Model did not return valid JSON.")
        raise

if __name__ == "__main__":
    url_input = "https://hackrx.blob.core.windows.net/assets/indian_constitution.pdf?somequery=123"
    questions_input = [
        "What is the official name of India according to Article 1 of the Constitution?",
        "Which Article guarantees equality before the law and equal protection of laws to all persons?",
        "What is abolished by Article 17 of the Constitution?",
        "What are the key ideals mentioned in the Preamble of the Constitution of India?",
        "Under which Article can Parliament alter the boundaries, area, or name of an existing State?",
        "According to Article 24, children below what age are prohibited from working in hazardous industries like factories or mines?",
        "What is the significance of Article 21 in the Indian Constitution?",
        "Article 15 prohibits discrimination on certain grounds. However, which groups can the State make special provisions for under this Article?",
        "Which Article allows Parliament to regulate the right of citizenship and override previous articles on citizenship (Articles 5 to 10)?",
        "What restrictions can the State impose on the right to freedom of speech under Article 19(2)?"
      ]

    answers = get_structured_answers(url_input, questions_input)
    print(answers)