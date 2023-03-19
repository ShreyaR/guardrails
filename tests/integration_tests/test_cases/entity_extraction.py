# flake8: noqa: E501

from guardrails.utils.reask_utils import ReAsk

COMPILED_PROMPT = '\nGiven the following document, answer the following questions. If the answer doesn\'t exist in the document, enter \'None\'.\n\n2/25/23, 7:59 PM about:blank\r\nabout:blank 1/4\r\nPRICING INFORMATION\r\nINTEREST RATES AND INTEREST CHARGES\r\nPurchase Annual\r\nPercentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open.\r\nAfter that, 19.49%. This APR will vary with the market based on the Prime\r\nRate.\r\na\r\nMy Chase Loan\r\nSM APR 19.49%. This APR will vary with the market based on the Prime Rate.\r\na\r\nPromotional offers with fixed APRs and varying durations may be available from\r\ntime to time on some accounts.\r\nBalance Transfer APR 0% Intro APR for the first 18 months that your Account is open.\r\nAfter that, 19.49%. This APR will vary with the market based on the Prime\r\nRate.\r\na\r\nCash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate.\r\nb\r\nPenalty APR and When\r\nIt Applies\r\nUp to 29.99%. This APR will vary with the market based on the Prime Rate.\r\nc\r\nWe may apply the Penalty APR to your account if you:\r\nfail to make a Minimum Payment by the date and time that it is due; or\r\nmake a payment to us that is returned unpaid.\r\nHow Long Will the Penalty APR Apply?: If we apply the Penalty APR for\r\neither of these reasons, the Penalty APR could potentially remain in effect\r\nindefinitely.\r\nHow to Avoid Paying\r\nInterest on Purchases\r\nYour due date will be a minimum of 21 days after the close of each billing cycle.\r\nWe will not charge you interest on new purchases if you pay your entire balance\r\nor Interest Saving Balance by the due date each month. We will begin charging\r\ninterest on balance transfers and cash advances on the transaction date.\r\nMinimum Interest\r\nCharge\r\nNone\r\nCredit Card Tips from\r\nthe Consumer Financial\r\nProtection Bureau\r\nTo learn more about factors to consider when applying for or using a credit card,\r\nvisit the website of the Consumer Financial Protection Bureau at\r\nhttp://www.consumerfinance.gov/learnmore.\r\nFEES\r\nAnnual Membership\r\nFee\r\nNone\r\nMy Chase Plan\r\nSM Fee\r\n(fixed finance charge)\r\nMonthly fee of 0% of the amount of each eligible purchase transaction or\r\namount selected to create a My Chase Plan while in the 0% Intro Purchase\r\nAPR period.\r\nAfter that, monthly fee of 1.72% of the amount of each eligible purchase\r\ntransaction or amount selected to create a My Chase Plan. The My Chase Plan\r\nFee will be determined at the time each My Chase Plan is created and will\r\nremain the same until the My Chase Plan is paid in full.\r\nd\r\nTransaction Fees\r\nBalance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater,\r\non transfers made within 60 days of account opening. After that: Either $5 or 5%\r\nof the amount of each transfer, whichever is greater.\r\nCash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.\n2/25/23, 7:59 PM about:blank\r\nabout:blank 2/4\r\nForeign Transactions 3% of the amount of each transaction in U.S. dollars.\r\nPenalty Fees\r\nLate Payment Up to $40.\r\nOver-the-Credit-Limit None\r\nReturn Payment Up to $40.\r\nReturn Check None\r\nNote: This account may not be eligible for balance transfers.\r\nLoss of Intro APR: We will end your introductory APR if any required Minimum Payment is 60 days late, and\r\napply the Penalty APR.\r\nHow We Will Calculate Your Balance: We use the daily balance method (including new transactions).\r\nPrime Rate: Variable APRs are based on the 7.75% Prime Rate as of 2/7/2023.\r\naWe add 11.74% to the Prime Rate to determine the Purchase/My Chase Loan/Balance Transfer APR.\r\nMaximum APR 29.99%.\r\nbWe add 21.74% to the Prime Rate to determine the Cash Advance APR. Maximum APR 29.99%.\r\ncWe add up to 26.99% to the Prime Rate to determine the Penalty APR. Maximum APR 29.99%.\r\ndMy Chase Plan Fee: The My Chase Plan Fee is calculated at the time each plan is created and is based on\r\nthe amount of each purchase transaction or amount selected to create the plan, the number of billing periods\r\nyou choose to pay the balance in full, and other factors. The monthly and aggregate dollar amount of your My\r\nChase Plan Fee will be disclosed during the activation of each My Chase Plan.\r\nMILITARY LENDING ACT NOTICE: Federal law provides important protections to members of the Armed\r\nForces and their dependents relating to extensions of consumer credit. In general, the cost of consumer credit\r\nto a member of the Armed Forces and his or her dependent may not exceed an annual percentage rate of 36\r\npercent. This rate must include, as applicable to the credit transaction or account: the costs associated with\r\ncredit insurance premiums; fees for ancillary products sold in connection with the credit transaction; any\r\napplication fee charged (other than certain application fees for specified credit transactions or accounts); and\r\nany participation fee charged (other than certain participation fees for a credit card account). To receive this\r\ninformation and a description of your payment obligation verbally, please call 1-800-235-9978.\r\nTERMS & CONDITIONS\r\nAuthorization: When you respond to this credit card offer from JPMorgan Chase Bank, N.A., Member FDIC, a\r\nsubsidiary of JPMorgan Chase & Co. ("Chase", "we", or "us"), you agree to the following:\r\n1. You authorize us to obtain credit bureau reports, employment, and income information about you that we\r\nwill use when considering your application for credit. We may obtain and use information about your\r\naccounts with us and others such as Checking, Deposit, Investment, and Utility accounts from credit\r\nbureaus and other entities. You also authorize us to obtain credit bureau reports and any other\r\ninformation about you in connection with: 1) extensions of credit on your account; 2) the administration,\r\nreview or collection of your account; and 3) offering you enhanced or additional products and services. If\r\nyou ask, we will tell you the name and address of the credit bureau from which we obtained a report\r\nabout you.\r\n2. If an account is opened, you will receive a Cardmember Agreement with your card(s). You agree to the\r\nterms of this agreement by: using the account\n\n\nGiven below is XML that describes the information to extract from this document and the tags to extract it into.\n\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <integer name="index" format="1-indexed"/>\n            <string name="name" format="lower-case; two-words"/>\n            <string name="explanation" format="one-line"/>\n            <float name="value" format="percentage"/>\n        </object>\n    </list>\n    <object name="interest_rates" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?"/>\n</output>\n\n\n\n\n\nONLY return a valid JSON object (no other text is necessary). The JSON MUST conform to the XML format, including any types and format requests e.g. requests for lists, objects and specific types. Be correct and concise.\n\nJSON Output:\n'


LLM_OUTPUT = '\n{\n  "fees": [\n    {\n      "index": 1,\n      "name": "annual membership",\n      "explanation": "Annual Membership Fee",\n      "value": 0\n    },\n    {\n      "index": 2,\n      "name": "my chase plan",\n      "explanation": "My Chase Plan Fee (fixed finance charge)",\n      "value": 1.72\n    },\n    {\n      "index": 3,\n      "name": "balance transfers",\n      "explanation": "Balance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater, on transfers made within 60 days of account opening. After that: Either $5 or 5% of the amount of each transfer.",\n      "value": 5\n    },\n    {\n      "index": 4,\n      "name": "cash advances",\n      "explanation": "Cash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.",\n      "value": 5\n    },\n    {\n      "index": 5,\n      "name": "foreign transactions",\n      "explanation": "Foreign Transactions 3% of the amount of each transaction in U.S. dollars.",\n      "value": 3\n    },\n    {\n      "index": 6,\n      "name": "late payment",\n      "explanation": "Late Payment Up to $40.",\n      "value": 0\n    },\n    {\n      "index": 7,\n      "name": "over-the-credit-limit",\n      "explanation": "Over-the-Credit-Limit None",\n      "value": 0\n    },\n    {\n      "index": 8,\n      "name": "return payment",\n      "explanation": "Return Payment Up to $40.",\n      "value": 0\n    },\n    {\n      "index": 9,\n      "name": "return check",\n      "explanation": "Return Check None",\n      "value": 0\n    }\n  ],\n  "interest_rates": {\n    "purchase": {\n      "apr": 0,\n      "explanation": "Purchase Annual Percentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate."\n    },\n    "my_chase_loan": {\n      "apr": 19.49,\n      "explanation": "My Chase Loan SM APR 19.49%. This APR will vary with the market based on the Prime Rate."\n    },\n    "balance_transfer": {\n      "apr": 0,\n      "explanation": "Balance Transfer APR 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate."\n    },\n    "cash_advance": {\n      "apr": 29.49,\n      "explanation": "Cash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate."\n    },\n    "penalty": {\n      "apr": 29.99,\n      "explanation": "Up to 29.99%. This APR will vary with the market based on the Prime Rate."\n    },\n    "maximum_apr": 29.99\n  }\n}'


COMPILED_PROMPT_REASK = '\nI was given the following JSON response, which had problems due to incorrect values.\n\n{\n  "fees": [\n    {\n      "name": {\n        "incorrect_value": "my chase plan",\n        "error_message": "must be exactly two words",\n        "fix_value": "my chase",\n        "path": [\n          "fees",\n          1,\n          "name"\n        ]\n      }\n    },\n    {\n      "name": {\n        "incorrect_value": "over-the-credit-limit",\n        "error_message": "must be exactly two words",\n        "fix_value": "over-the-credit-limit",\n        "path": [\n          "fees",\n          6,\n          "name"\n        ]\n      }\n    }\n  ]\n}\n\nHelp me correct the incorrect values based on the given error messages.\n\nGiven below is XML that describes the information to extract from this document and the tags to extract it into.\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <string name="name" format="lower-case; two-words"/>\n            </object>\n    </list>\n    </output>\n\n\n\n\nONLY return a valid JSON object (no other text is necessary), where the key of the field in JSON is the `name` attribute of the corresponding XML, and the value is of the type specified by the corresponding XML\'s tag. The JSON MUST conform to the XML format, including any types and format requests e.g. requests for lists, objects and specific types. Be correct and concise. If you are unsure anywhere, enter `None`.\n\nHere are examples of simple (XML, JSON) pairs that show the expected behavior:\n- `<string name=\'foo\' format=\'two-words lower-case\' />` => `{{\'foo\': \'example one\'}}`\n- `<list name=\'bar\'><string format=\'upper-case\' /></list>` => `{{"bar": [\'STRING ONE\', \'STRING TWO\', etc.]}}`\n- `<object name=\'baz\'><string name="foo" format="capitalize two-words" /><integer name="index" format="1-indexed" /></object>` => `{{\'baz\': {{\'foo\': \'Some String\', \'index\': 1}}}}`\n\nJSON Object:'


LLM_OUTPUT_REASK = '\n{\n  "fees": [\n    {\n      "name": "my chase"\n    },\n    {\n      "name": "over-the-credit-limit"\n    }\n  ]\n}'


RAIL_SPEC_WITH_REASK = '\n<rail version="0.1">\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <integer name="index" format="1-indexed" />\n            <string name="name" format="lower-case; two-words" on-fail-lower-case="noop" on-fail-two-words="reask"/>\n            <string name="explanation" format="one-line" on-fail-one-line="noop" />\n            <float name="value" format="percentage"/>\n        </object>\n    </list>\n    <object name="interest_rates" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?" />\n</output>\n\n\n<prompt>\nGiven the following document, answer the following questions. If the answer doesn\'t exist in the document, enter \'None\'.\n\n{{document}}\n\n@xml_prefix_prompt\n\n{output_schema}\n\n@json_suffix_prompt_v2_wo_none</prompt>\n\n</rail>\n'


VALIDATED_OUTPUT_REASK_1 = {
    "fees": [
        {
            "index": 1,
            "name": "annual membership",
            "explanation": "Annual Membership Fee",
            "value": 0,
        },
        {
            "index": 2,
            "name": ReAsk(
                incorrect_value="my chase plan",
                error_message="must be exactly two words",
                fix_value="my chase",
                path=["fees", 1, "name"],
            ),
            "explanation": "My Chase Plan Fee (fixed finance charge)",
            "value": 1.72,
        },
        {
            "index": 3,
            "name": "balance transfers",
            "explanation": "Balance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater, on transfers made within 60 days of account opening. After that: Either $5 or 5% of the amount of each transfer.",
            "value": 5,
        },
        {
            "index": 4,
            "name": "cash advances",
            "explanation": "Cash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.",
            "value": 5,
        },
        {
            "index": 5,
            "name": "foreign transactions",
            "explanation": "Foreign Transactions 3% of the amount of each transaction in U.S. dollars.",
            "value": 3,
        },
        {
            "index": 6,
            "name": "late payment",
            "explanation": "Late Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 7,
            "name": ReAsk(
                incorrect_value="over-the-credit-limit",
                error_message="must be exactly two words",
                fix_value="over-the-credit-limit",
                path=["fees", 6, "name"],
            ),
            "explanation": "Over-the-Credit-Limit None",
            "value": 0,
        },
        {
            "index": 8,
            "name": "return payment",
            "explanation": "Return Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 9,
            "name": "return check",
            "explanation": "Return Check None",
            "value": 0,
        },
    ],
    "interest_rates": {
        "purchase": {
            "apr": 0,
            "explanation": "Purchase Annual Percentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "my_chase_loan": {
            "apr": 19.49,
            "explanation": "My Chase Loan SM APR 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "balance_transfer": {
            "apr": 0,
            "explanation": "Balance Transfer APR 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "cash_advance": {
            "apr": 29.49,
            "explanation": "Cash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "penalty": {
            "apr": 29.99,
            "explanation": "Up to 29.99%. This APR will vary with the market based on the Prime Rate.",
        },
        "maximum_apr": 29.99,
    },
}


VALIDATED_OUTPUT_REASK_2 = {
    "fees": [
        {
            "index": 1,
            "name": "annual membership",
            "explanation": "Annual Membership Fee",
            "value": 0,
        },
        {
            "index": 2,
            "name": "my chase",
            "explanation": "My Chase Plan Fee (fixed finance charge)",
            "value": 1.72,
        },
        {
            "index": 3,
            "name": "balance transfers",
            "explanation": "Balance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater, on transfers made within 60 days of account opening. After that: Either $5 or 5% of the amount of each transfer.",
            "value": 5,
        },
        {
            "index": 4,
            "name": "cash advances",
            "explanation": "Cash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.",
            "value": 5,
        },
        {
            "index": 5,
            "name": "foreign transactions",
            "explanation": "Foreign Transactions 3% of the amount of each transaction in U.S. dollars.",
            "value": 3,
        },
        {
            "index": 6,
            "name": "late payment",
            "explanation": "Late Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 7,
            "name": "over-the-credit-limit",
            "explanation": "Over-the-Credit-Limit None",
            "value": 0,
        },
        {
            "index": 8,
            "name": "return payment",
            "explanation": "Return Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 9,
            "name": "return check",
            "explanation": "Return Check None",
            "value": 0,
        },
    ],
    "interest_rates": {
        "purchase": {
            "apr": 0,
            "explanation": "Purchase Annual Percentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "my_chase_loan": {
            "apr": 19.49,
            "explanation": "My Chase Loan SM APR 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "balance_transfer": {
            "apr": 0,
            "explanation": "Balance Transfer APR 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "cash_advance": {
            "apr": 29.49,
            "explanation": "Cash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "penalty": {
            "apr": 29.99,
            "explanation": "Up to 29.99%. This APR will vary with the market based on the Prime Rate.",
        },
        "maximum_apr": 29.99,
    },
}


RAIL_SPEC_WITH_NOOP = '\n<rail version="0.1">\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <integer name="index" format="1-indexed" />\n            <string name="name" format="lower-case; two-words" on-fail-lower-case="noop" on-fail-two-words="noop"/>\n            <string name="explanation" format="one-line" on-fail-one-line="noop" />\n            <float name="value" format="percentage"/>\n        </object>\n    </list>\n    <object name="interest_rates" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?" />\n</output>\n\n\n<prompt>\nGiven the following document, answer the following questions. If the answer doesn\'t exist in the document, enter \'None\'.\n\n{{document}}\n\n@xml_prefix_prompt\n\n{output_schema}\n\n@json_suffix_prompt_v2_wo_none</prompt>\n\n</rail>\n'


VALIDATED_OUTPUT_NOOP = {
    "fees": [
        {
            "index": 1,
            "name": "annual membership",
            "explanation": "Annual Membership Fee",
            "value": 0,
        },
        {
            "index": 2,
            "name": "my chase plan",
            "explanation": "My Chase Plan Fee (fixed finance charge)",
            "value": 1.72,
        },
        {
            "index": 3,
            "name": "balance transfers",
            "explanation": "Balance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater, on transfers made within 60 days of account opening. After that: Either $5 or 5% of the amount of each transfer.",
            "value": 5,
        },
        {
            "index": 4,
            "name": "cash advances",
            "explanation": "Cash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.",
            "value": 5,
        },
        {
            "index": 5,
            "name": "foreign transactions",
            "explanation": "Foreign Transactions 3% of the amount of each transaction in U.S. dollars.",
            "value": 3,
        },
        {
            "index": 6,
            "name": "late payment",
            "explanation": "Late Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 7,
            "name": "over-the-credit-limit",
            "explanation": "Over-the-Credit-Limit None",
            "value": 0,
        },
        {
            "index": 8,
            "name": "return payment",
            "explanation": "Return Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 9,
            "name": "return check",
            "explanation": "Return Check None",
            "value": 0,
        },
    ],
    "interest_rates": {
        "purchase": {
            "apr": 0,
            "explanation": "Purchase Annual Percentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "my_chase_loan": {
            "apr": 19.49,
            "explanation": "My Chase Loan SM APR 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "balance_transfer": {
            "apr": 0,
            "explanation": "Balance Transfer APR 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "cash_advance": {
            "apr": 29.49,
            "explanation": "Cash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "penalty": {
            "apr": 29.99,
            "explanation": "Up to 29.99%. This APR will vary with the market based on the Prime Rate.",
        },
        "maximum_apr": 29.99,
    },
}


RAIL_SPEC_WITH_FILTER = '\n<rail version="0.1">\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <integer name="index" format="1-indexed" />\n            <string name="name" format="lower-case; two-words" on-fail-lower-case="filter" on-fail-two-words="filter"/>\n            <string name="explanation" format="one-line" on-fail-one-line="filter" />\n            <float name="value" format="percentage"/>\n        </object>\n    </list>\n    <object name="interest_rates" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?" />\n</output>\n\n\n<prompt>\nGiven the following document, answer the following questions. If the answer doesn\'t exist in the document, enter \'None\'.\n\n{{document}}\n\n@xml_prefix_prompt\n\n{output_schema}\n\n@json_suffix_prompt_v2_wo_none</prompt>\n\n</rail>\n'


VALIDATED_OUTPUT_FILTER = {
    "fees": [
        {
            "index": 1,
            "name": "annual membership",
            "explanation": "Annual Membership Fee",
            "value": 0,
        },
        {
            "index": 2,
            "explanation": "My Chase Plan Fee (fixed finance charge)",
            "value": 1.72,
        },
        {
            "index": 3,
            "name": "balance transfers",
            "explanation": "Balance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater, on transfers made within 60 days of account opening. After that: Either $5 or 5% of the amount of each transfer.",
            "value": 5,
        },
        {
            "index": 4,
            "name": "cash advances",
            "explanation": "Cash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.",
            "value": 5,
        },
        {
            "index": 5,
            "name": "foreign transactions",
            "explanation": "Foreign Transactions 3% of the amount of each transaction in U.S. dollars.",
            "value": 3,
        },
        {
            "index": 6,
            "name": "late payment",
            "explanation": "Late Payment Up to $40.",
            "value": 0,
        },
        {"index": 7, "explanation": "Over-the-Credit-Limit None", "value": 0},
        {
            "index": 8,
            "name": "return payment",
            "explanation": "Return Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 9,
            "name": "return check",
            "explanation": "Return Check None",
            "value": 0,
        },
    ],
    "interest_rates": {
        "purchase": {
            "apr": 0,
            "explanation": "Purchase Annual Percentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "my_chase_loan": {
            "apr": 19.49,
            "explanation": "My Chase Loan SM APR 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "balance_transfer": {
            "apr": 0,
            "explanation": "Balance Transfer APR 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "cash_advance": {
            "apr": 29.49,
            "explanation": "Cash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "penalty": {
            "apr": 29.99,
            "explanation": "Up to 29.99%. This APR will vary with the market based on the Prime Rate.",
        },
        "maximum_apr": 29.99,
    },
}


RAIL_SPEC_WITH_FIX = '\n<rail version="0.1">\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <integer name="index" format="1-indexed" />\n            <string name="name" format="lower-case; two-words" on-fail-lower-case="fix" on-fail-two-words="fix"/>\n            <string name="explanation" format="one-line" on-fail-one-line="fix" />\n            <float name="value" format="percentage"/>\n        </object>\n    </list>\n    <object name="interest_rates" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?" />\n</output>\n\n\n<prompt>\nGiven the following document, answer the following questions. If the answer doesn\'t exist in the document, enter \'None\'.\n\n{{document}}\n\n@xml_prefix_prompt\n\n{output_schema}\n\n@json_suffix_prompt_v2_wo_none</prompt>\n\n</rail>\n'


VALIDATED_OUTPUT_FIX = {
    "fees": [
        {
            "index": 1,
            "name": "annual membership",
            "explanation": "Annual Membership Fee",
            "value": 0,
        },
        {
            "index": 2,
            "name": "my chase",
            "explanation": "My Chase Plan Fee (fixed finance charge)",
            "value": 1.72,
        },
        {
            "index": 3,
            "name": "balance transfers",
            "explanation": "Balance Transfers Intro fee of either $5 or 3% of the amount of each transfer, whichever is greater, on transfers made within 60 days of account opening. After that: Either $5 or 5% of the amount of each transfer.",
            "value": 5,
        },
        {
            "index": 4,
            "name": "cash advances",
            "explanation": "Cash Advances Either $10 or 5% of the amount of each transaction, whichever is greater.",
            "value": 5,
        },
        {
            "index": 5,
            "name": "foreign transactions",
            "explanation": "Foreign Transactions 3% of the amount of each transaction in U.S. dollars.",
            "value": 3,
        },
        {
            "index": 6,
            "name": "late payment",
            "explanation": "Late Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 7,
            "name": "over-the-credit-limit",
            "explanation": "Over-the-Credit-Limit None",
            "value": 0,
        },
        {
            "index": 8,
            "name": "return payment",
            "explanation": "Return Payment Up to $40.",
            "value": 0,
        },
        {
            "index": 9,
            "name": "return check",
            "explanation": "Return Check None",
            "value": 0,
        },
    ],
    "interest_rates": {
        "purchase": {
            "apr": 0,
            "explanation": "Purchase Annual Percentage Rate (APR) 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "my_chase_loan": {
            "apr": 19.49,
            "explanation": "My Chase Loan SM APR 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "balance_transfer": {
            "apr": 0,
            "explanation": "Balance Transfer APR 0% Intro APR for the first 18 months that your Account is open. After that, 19.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "cash_advance": {
            "apr": 29.49,
            "explanation": "Cash Advance APR 29.49%. This APR will vary with the market based on the Prime Rate.",
        },
        "penalty": {
            "apr": 29.99,
            "explanation": "Up to 29.99%. This APR will vary with the market based on the Prime Rate.",
        },
        "maximum_apr": 29.99,
    },
}


RAIL_SPEC_WITH_REFRAIN = '\n<rail version="0.1">\n\n<output>\n\n    <list name="fees" description="What fees and charges are associated with my account?">\n        <object>\n            <integer name="index" format="1-indexed" />\n            <string name="name" format="lower-case; two-words" on-fail-lower-case="refrain" on-fail-two-words="refrain"/>\n            <string name="explanation" format="one-line" on-fail-one-line="refrain" />\n            <float name="value" format="percentage"/>\n        </object>\n    </list>\n    <object name="interest_rates" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?" />\n</output>\n\n\n<prompt>\nGiven the following document, answer the following questions. If the answer doesn\'t exist in the document, enter \'None\'.\n\n{{document}}\n\n@xml_prefix_prompt\n\n{output_schema}\n\n@json_suffix_prompt_v2_wo_none</prompt>\n\n</rail>\n'


VALIDATED_OUTPUT_REFRAIN = {}
