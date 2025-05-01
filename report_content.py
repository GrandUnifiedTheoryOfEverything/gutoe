#!/usr/bin/env python3
"""
Report Content Generator

This script generates sample report content for the Augmentic PDF Agent.
"""

import json
from augmentic_pdf_agent import PDFAgent

# Create sample report content
report_content = {
    "title": "Quantum Computing: Market Analysis and Future Trends",
    "subtitle": "Strategic Insights for Technology Investment",
    "executive_summary": (
        "This report provides a comprehensive analysis of the quantum computing market, "
        "including current technologies, major players, investment trends, and future projections. "
        "Our research indicates that the global quantum computing market is expected to grow "
        "at a CAGR of 25.4% from 2023 to 2030, reaching approximately $64.6 billion by 2030. "
        "Key growth drivers include increasing investments from both public and private sectors, "
        "advancements in quantum hardware, and expanding applications across industries such as "
        "pharmaceuticals, finance, cybersecurity, and artificial intelligence.\n\n"
        "We recommend strategic investments in quantum computing infrastructure, talent acquisition, "
        "and research partnerships to capitalize on this emerging technology revolution."
    ),
    "sections": [
        {
            "title": "Market Overview",
            "text": (
                "The quantum computing market has experienced significant growth in recent years, "
                "driven by technological advancements and increasing recognition of quantum computing's "
                "potential to solve complex problems beyond the capabilities of classical computers. "
                "As of 2023, the global quantum computing market is valued at approximately $12.3 billion, "
                "with North America representing the largest market share (42%), followed by Europe (28%) "
                "and Asia-Pacific (24%).\n\n"
                "Major segments within the quantum computing market include:"
            ),
            "bullet_list": [
                "Hardware (quantum processors, cryogenic systems, control electronics)",
                "Software (quantum algorithms, development tools, simulation platforms)",
                "Services (consulting, implementation, managed services)",
                "Applications (optimization, machine learning, cryptography, material science)"
            ],
            "table": [
                ["Region", "Market Share (%)", "CAGR (2023-2030)"],
                ["North America", "42%", "24.8%"],
                ["Europe", "28%", "26.2%"],
                ["Asia-Pacific", "24%", "27.5%"],
                ["Rest of World", "6%", "22.1%"]
            ],
            "table_caption": "Table 1: Quantum Computing Market Distribution by Region"
        },
        {
            "title": "Key Players and Competitive Landscape",
            "text": (
                "The quantum computing landscape features a mix of established technology giants, "
                "specialized quantum startups, and research institutions. Key players can be categorized "
                "into hardware providers, software developers, and end-to-end solution providers.\n\n"
                "Major companies in the quantum computing space include:"
            ),
            "bullet_list": [
                {
                    "text": "Hardware Providers",
                    "subitems": [
                        "IBM Quantum",
                        "Google Quantum AI",
                        "Rigetti Computing",
                        "IonQ",
                        "D-Wave Systems"
                    ]
                },
                {
                    "text": "Software Developers",
                    "subitems": [
                        "QC Ware",
                        "Zapata Computing",
                        "Cambridge Quantum Computing",
                        "1QBit",
                        "Strangeworks"
                    ]
                },
                {
                    "text": "End-to-End Solution Providers",
                    "subitems": [
                        "IBM",
                        "Microsoft Azure Quantum",
                        "Amazon Braket",
                        "Honeywell Quantum Solutions",
                        "Xanadu"
                    ]
                }
            ]
        },
        {
            "title": "Investment Trends",
            "text": (
                "Investment in quantum computing has accelerated significantly in recent years, "
                "with both public and private funding reaching record levels. Government initiatives "
                "worldwide have allocated billions of dollars to quantum research and development, "
                "while venture capital investment in quantum startups has grown at an annual rate "
                "of approximately 40% since 2018.\n\n"
                "Notable investment trends include:"
            ),
            "bullet_list": [
                "Increasing corporate venture capital participation from technology and financial sectors",
                "Growing number of SPAC mergers and public listings for quantum computing companies",
                "Expansion of government funding programs in the US, EU, China, UK, and Japan",
                "Rising investments in quantum-specific talent development and educational initiatives"
            ]
        },
        {
            "title": "Applications and Use Cases",
            "text": (
                "Quantum computing applications span numerous industries, with early adopters "
                "focusing on problems that are computationally intensive and have high potential "
                "business impact. Key application areas include:"
            ),
            "bullet_list": [
                "Pharmaceutical and materials research (drug discovery, molecular modeling)",
                "Financial services (portfolio optimization, risk analysis, fraud detection)",
                "Logistics and supply chain (route optimization, scheduling, inventory management)",
                "Artificial intelligence and machine learning (quantum neural networks, pattern recognition)",
                "Cybersecurity (post-quantum cryptography, secure communications)"
            ]
        }
    ],
    "conclusion": (
        "Quantum computing represents a transformative technology with the potential to revolutionize "
        "numerous industries by solving previously intractable problems. While still in its early stages, "
        "the quantum computing market is poised for substantial growth over the next decade.\n\n"
        "Organizations seeking to capitalize on quantum computing should consider a phased approach: "
        "building quantum literacy and expertise, identifying high-value use cases, engaging with the "
        "quantum ecosystem through partnerships, and developing a long-term quantum strategy aligned "
        "with business objectives. Early movers in this space will likely gain significant competitive "
        "advantages as quantum technologies mature and become more accessible."
    ),
    "appendices": [
        {
            "title": "Quantum Computing Glossary",
            "text": (
                "Qubit: The fundamental unit of quantum information, analogous to a classical bit but capable "
                "of existing in superposition states.\n\n"
                "Quantum Supremacy: The point at which a quantum computer can solve a problem that is practically "
                "impossible for classical computers to solve in a reasonable timeframe.\n\n"
                "Quantum Gate: The basic quantum circuit operating on a small number of qubits, analogous to "
                "classical logic gates.\n\n"
                "Quantum Annealing: A quantum computing approach used to find the global minimum of a given "
                "objective function, particularly suited for optimization problems.\n\n"
                "Quantum Error Correction: Techniques to protect quantum information from errors due to "
                "decoherence and other quantum noise."
            )
        },
        {
            "title": "Research Methodology",
            "text": (
                "This report is based on comprehensive primary and secondary research conducted between "
                "January and March 2023. Our methodology included:\n\n"
                "- Interviews with 45+ quantum computing experts, including researchers, executives, "
                "investors, and end-users\n"
                "- Analysis of financial data from public companies and venture capital databases\n"
                "- Review of academic publications, patents, and technical documentation\n"
                "- Evaluation of government policies and funding initiatives\n"
                "- Survey of 200+ potential enterprise quantum computing users across industries"
            )
        }
    ]
}

# Create PDF agent and generate report
if __name__ == "__main__":
    agent = PDFAgent()
    pdf_path = agent.create_report(
        report_content["title"],
        report_content,
        "quantum_computing_report.pdf"
    )
    print(f"Professional report created: {pdf_path}")
