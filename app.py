from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# API field configurations
api_fields = {
    "Choose the API": [],
    "Send Transaction": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "AGENT_TXNID", "LOCATION_ID",
        "SENDER_FIRST_NAME", "SENDER_MIDDLE_NAME", "SENDER_LAST_NAME", "SENDER_GENDER",
        "SENDER_ADDRESS", "SENDER_CITY", "SENDER_COUNTRY", "SENDER_ID_TYPE",
        "SENDER_ID_NUMBER", "SENDER_ID_ISSUE_DATE", "SENDER_ID_EXPIRE_DATE",
        "SENDER_DATE_OF_BIRTH", "SENDER_MOBILE", "SOURCE_OF_FUND", "SENDER_OCCUPATION",
        "SENDER_NATIONALITY", "RECEIVER_FIRST_NAME", "RECEIVER_MIDDLE_NAME",
        "RECEIVER_LAST_NAME", "RECEIVER_ADDRESS", "RECEIVER_CITY", "RECEIVER_COUNTRY",
        "RECEIVER_CONTACT_NUMBER", "RELATIONSHIP_TO_BENEFICIARY", "PAYMENT_MODE",
        "BANK_ID", "BANK_NAME", "BANK_BRANCH_NAME", "BANK_ACCOUNT_NUMBER", "WALLET_ID",
        "CALC_BY", "TRANSFER_AMOUNT", "OURSERVICE_CHARGE", "TRANSACTION_EXCHANGERATE",
        "SETTLEMENT_DOLLARRATE", "PURPOSE_OF_REMITTANCE", "ADDITIONAL_FIELD1",
        "ADDITIONAL_FIELD2", "AUTHORIZED_REQUIRED", "API_PASSWORD"
    ],
    "Account Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PAYMENT_MODE", "BankCode",
        "AccountNumber", "AccountName", "API_PASSWORD"
    ],
    "Get Exchange Rate": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "TRANSFER_AMOUNT", "PAYMENT_MODE",
        "CALC_BY","LOCATION_ID","PAYOUT_COUNTRY", "API_PASSWORD"
    ],
    "SSF Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PAYMENT_MODE", "BankCode",
        "PSSID", "API_PASSWORD"
    ],
    "Wallet Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "WalletId", "AccountName",
        "TransferAmount", "API_PASSWORD"
    ],
    "Fonepay Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PAYMENT_MODE", "BankCode", "MobileNumber", "API_PASSWORD"
    ],
    "Ammendment Request": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PINNO", "AMENDMENT_FIELD",
        "AMENDMENT_VALUE", "API_PASSWORD"
    ],
    "Authorized Confirmed": [
        "AGENT_CODE", "USER_ID", "PINNO", "AGENT_SESSION_ID", "API_PASSWORD"
    ],
    "Cancel Transaction": [
        "AGENT_CODE", "USER_ID", "PINNO",  "AGENT_SESSION_ID", "CANCEL_REASON", "API_PASSWORD"
    ],
    "Get Current Balance": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "API_PASSWORD"
    ],
    "Query Txn Status": [
        "AGENT_CODE", "USER_ID", "PINNO",  "AGENT_SESSION_ID", "AGENT_TXNID", "API_PASSWORD"
    ]
}

@app.route("/generate", methods=["POST"])
def generate_signature():
    data = request.json
    selected_api = data.get("api")
    fields = api_fields.get(selected_api, [])

    values = {field: data.get(field, "") for field in fields}

    # Only generate hash if at least one field has a value
    if not selected_api or not fields or not any(values.values()):
        return jsonify({
            "success": False,
            "message": "No API selected or no field values provided."
        })

    concatenated = "".join([values[field] for field in fields])
    signature = hashlib.sha256(concatenated.encode()).hexdigest()

    return jsonify({
        "success": True,
        "concatenated": concatenated,
        "signature": signature
    })

if __name__ == "__main__":
    app.run(debug=True)
