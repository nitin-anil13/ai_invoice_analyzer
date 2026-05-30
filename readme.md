# 💼 AI Invoice Risk Analyzer

An AI-powered document orchestration system that extracts critical information from unstructured invoices, evaluates invoice risk using a custom rule-based scoring engine, and automatically sends analysis reports via n8n email automation.

---

## 📌 Overview

Businesses receive invoices in different formats, making manual verification slow and prone to errors. This project automates invoice analysis by combining AI-based data extraction with a transparent risk assessment model.

The system:

- Extracts key invoice details from PDFs and text files.
- Converts unstructured invoice data into structured JSON.
- Calculates invoice risk using predefined business rules.
- Generates an easy-to-understand risk report.
- Sends the report automatically via email using n8n workflows.

---

## 🚀 Features

### 📄 Invoice Processing
- Supports PDF invoices
- Supports TXT documents
- Handles unstructured and messy invoice formats

### 🤖 AI-Based Data Extraction
The AI model extracts:

- Vendor Name
- Invoice Number
- Invoice Date
- Due Date
- Total Amount
- Currency
- Payment Status

### 📊 Rule-Based Risk Analysis
Unlike traditional AI risk predictions, risk levels are calculated using fixed business rules to ensure:

- Transparency
- Consistency
- Explainability
- Reliability

### 📧 Automated Email Reporting
Users can send invoice analysis reports directly from the application.

n8n automation handles:

- Report generation
- Email formatting
- Email delivery
- Workflow automation

---

## 🏗️ System Architecture

```text
Invoice Upload
      │
      ▼
Text Extraction
(PDFPlumber)
      │
      ▼
AI Data Extraction
(Groq Llama 3.3)
      │
      ▼
Structured JSON
      │
      ▼
Risk Analysis Engine
(Custom Rules)
      │
      ▼
Risk Report
      │
      ▼
n8n Webhook
      │
      ▼
Automated Email Delivery
```

---

## ⚙️ Risk Calculation Logic

### Rule 1: High Invoice Amount

If:

```text
Amount > 50,000
```

Score:

```text
+40
```

### Rule 2: Pending Payment

If payment status contains:

- Pending
- Unpaid
- Not Cleared

Score:

```text
+30
```

### Rule 3: Due Date Present

If a due date exists:

```text
+30
```

### Risk Levels

| Score | Risk Level |
|---------|-----------|
| 0-39 | Low |
| 40-69 | Medium |
| 70-100 | High |

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Model
- Groq API
- Llama 3.3 70B Versatile

### Document Processing
- PDFPlumber
- JSON

### Automation
- n8n
- Webhooks

### Communication
- Requests Library

---

## 📂 Project Structure

```bash
AI-Invoice-Risk-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Invoice-Risk-Analyzer.git

cd AI-Invoice-Risk-Analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Secrets

Create:

```bash
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY="your_groq_api_key"

N8N_WEBHOOK_URL="your_n8n_webhook_url"
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## 📈 Sample Output

### Extracted Data

```json
{
  "vendor_name": "ABC Suppliers",
  "invoice_number": "INV-2026-101",
  "invoice_date": "2026-05-10",
  "due_date": "2026-06-10",
  "total_amount": "₹55,480",
  "currency": "INR",
  "payment_status": "Pending"
}
```

### Risk Analysis

```text
Risk Score: 100/100

Risk Level: HIGH

Reasons:
• High invoice amount
• Payment is pending
• Due date present
```

---

## 🔄 n8n Workflow

The application integrates with n8n using a webhook.

Workflow Steps:

1. Receive invoice analysis data from Streamlit.
2. Process the incoming JSON payload.
3. Generate a formatted email report.
4. Send the report to the specified email address.
5. Return a success response to the application.

---

## 🎯 Business Benefits

- Reduces manual invoice review effort.
- Detects potentially risky invoices instantly.
- Improves financial oversight.
- Automates report sharing.
- Enhances operational efficiency.

---

## 🔮 Future Enhancements

- OCR support for scanned invoices
- Batch invoice processing
- Fraud detection models
- Vendor risk profiling
- Dashboard analytics
- Database integration
- Approval workflow automation

---

## 👨‍💻 Author

**Nithin V Anil**

B.Tech Computer Science

Interests:
- Artificial Intelligence
- Automation
- Data Analytics
- Business Intelligence

---

⭐ If you found this project useful, consider giving it a star on GitHub.
