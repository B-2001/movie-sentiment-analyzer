# Mini-Report: Movie Sentiment Analysis

## Prompt Design Choices
Used few-shot prompting with 3 clear examples (Positive, Negative, Neutral) to guide Gemini LLM. Examples chosen for unambiguous sentiment expression. Prompt explicitly requests structured JSON output with specific fields (label, confidence, explanation, evidence_phrases) for consistent formatting.

**Few-shot examples:**
- Positive: "This movie was absolutely fantastic! The acting was superb..."
- Negative: "Terrible film. Poor acting, boring plot..."  
- Neutral: "It was okay. Nothing special but not bad either..."

## Failure Cases & Mitigation
**Potential failures:** Sarcasm ("Oh great, another masterpiece..." → misclassified as Positive), mixed sentiments ("Great acting but terrible story" → handled as Neutral), short reviews ("Good movie" → lower confidence).

**Mitigation strategies:** Robust error handling with fallback to Neutral, JSON parsing with validation, input validation for empty reviews, rate limiting (1s delay between API calls).

## Performance Metrics
| Metric | Value | Details |
|--------|-------|---------|
| **Accuracy** | 100.00% | Perfect classification |
| **Test Set** | 10 reviews | 3 Positive, 3 Negative, 4 Neutral |
| **Avg Confidence** | 0.89 | High reliability |
| **Processing Time** | < 3s/review | Meets latency target |

**Confidence Distribution:** Positive: 0.96, Negative: 0.95, Neutral: 0.80

**Classification Report:**
             precision    recall  f1-score   support
Negative       1.00      1.00      1.00         3
 Neutral       1.00      1.00      1.00         4
Positive       1.00      1.00      1.00         3
accuracy                           1.00        10



**Per-Class Accuracy:** Positive: 100% (3/3), Negative: 100% (3/3), Neutral: 100% (4/4)

## Observations
Neutral reviews showed lower confidence (0.80 vs 0.95+ for Positive/Negative) due to mixed sentiment elements creating classification ambiguity. System achieved perfect 100% accuracy across all categories with high confidence scores, demonstrating effective prompt design and reliable sentiment classification.

## Limitations

- API dependency (requires internet)
- Subjectivity in sentiment classification
- Language limitations (primarily English)

## Future Enhancements

- Confidence calibration
- Multi-language support
- Sentiment intensity scoring
- Historical analysis tracking