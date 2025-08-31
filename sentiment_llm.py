import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import time
import pandas as pd
from typing import Dict, List

class SentimentAnalyzer:
    def __init__(self, model_name: str = "gemini-2.0-flash", temperature: float = 0.1):
        """
        Initialize the Gemini model for sentiment analysis
        """
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature
        
        # Few-shot examples for better performance
        self.few_shot_examples = """
        Examples:
        
        Review: "This movie was absolutely fantastic! The acting was superb and the storyline kept me engaged throughout."
        Sentiment: Positive
        Evidence: "fantastic", "superb acting", "engaging storyline"
        
        Review: "Terrible film. Poor acting, boring plot, and wasted my time completely."
        Sentiment: Negative  
        Evidence: "Terrible", "poor acting", "boring plot", "wasted my time"
        
        Review: "It was okay. Nothing special but not bad either. The cinematography was decent."
        Sentiment: Neutral
        Evidence: "okay", "nothing special", "not bad", "decent cinematography"
        """
    
    def analyze_sentiment(self, review_text: str) -> Dict:
        """
        Analyze sentiment of a movie review using Gemini LLM
        """
        # Input validation
        if not review_text or not isinstance(review_text, str) or review_text.strip() == "":
            return {
                "label": "Neutral",
                "confidence": 0.0,
                "explanation": "Invalid input: empty or non-string review",
                "evidence_phrases": []
            }
        
        prompt = f"""
        Analyze the sentiment of this movie review and provide:
        1. Sentiment label: Positive, Negative, or Neutral
        2. Confidence score between 0-1
        3. Brief explanation (1-2 sentences)
        4. 2-3 key evidence phrases from the text that support your analysis
        
        {self.few_shot_examples}
        
        Review: "{review_text}"
        
        Return ONLY a valid JSON object with this exact structure:
        {{
            "label": "Positive|Negative|Neutral",
            "confidence": 0.00,
            "explanation": "short reason",
            "evidence_phrases": ["phrase1", "phrase2"]
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=200
                )
            )
            
            # Extract JSON from response
            result_text = response.text.strip()
            
            # Clean the response
            if result_text.startswith('```json'):
                result_text = result_text[7:-3]  # Remove ```json and ```
            elif result_text.startswith('```'):
                result_text = result_text[3:-3]  # Remove ``` and ```
            
            result = json.loads(result_text)
            
            # Validate the response structure
            required_keys = ["label", "confidence", "explanation", "evidence_phrases"]
            if not all(key in result for key in required_keys):
                raise ValueError("Invalid response format from LLM")
                
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response.text if 'response' in locals() else 'No response'}")
            return {
                "label": "Neutral",
                "confidence": 0.0,
                "explanation": "JSON parsing error in analysis",
                "evidence_phrases": []
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                "label": "Neutral",
                "confidence": 0.0,
                "explanation": "Error in analysis",
                "evidence_phrases": []
            }
    
    def batch_analyze(self, reviews: List[str]) -> List[Dict]:
        """
        Analyze multiple reviews in sequence
        """
        results = []
        for i, review in enumerate(reviews):
            print(f"Analyzing review {i+1}/{len(reviews)}")
            result = self.analyze_sentiment(review)
            results.append(result)
            time.sleep(1)  # Rate limiting
            
        return results

def process_csv_file(input_csv: str, output_csv: str):
    """
    Process a CSV file with reviews and save results - FIXED VERSION
    """
    analyzer = SentimentAnalyzer()
    
    # Read input CSV
    df = pd.read_csv(input_csv)
    
    # Analyze each review
    results = analyzer.batch_analyze(df['review_text'].tolist())
    
    # Create new columns for the results - FIXED APPROACH
    df['predicted_label'] = [result['label'] for result in results]
    df['confidence_score'] = [result['confidence'] for result in results]
    df['explanation'] = [result['explanation'] for result in results]
    df['evidence_phrases'] = [', '.join(result['evidence_phrases']) for result in results]
    
    # Save results
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
    print(f"Successfully processed {len(df)} reviews")
    
    return df

# Alternative batch processing function with better error handling
def process_csv_file_robust(input_csv: str, output_csv: str):
    """
    More robust version with individual error handling per review
    """
    analyzer = SentimentAnalyzer()
    
    # Read input CSV
    df = pd.read_csv(input_csv)
    
    # Initialize new columns
    df['predicted_label'] = 'Pending'
    df['confidence_score'] = 0.0
    df['explanation'] = ''
    df['evidence_phrases'] = ''
    
    # Analyze each review individually with error handling
    for i, review_text in enumerate(df['review_text']):
        try:
            print(f"Analyzing review {i+1}/{len(df)}: {review_text[:50]}...")
            result = analyzer.analyze_sentiment(str(review_text))
            
            # Add results to dataframe
            df.at[i, 'predicted_label'] = result['label']
            df.at[i, 'confidence_score'] = result['confidence']
            df.at[i, 'explanation'] = result['explanation']
            df.at[i, 'evidence_phrases'] = ', '.join(result['evidence_phrases'])
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Error processing review {i+1}: {e}")
            df.at[i, 'predicted_label'] = 'Error'
            df.at[i, 'confidence_score'] = 0.0
            df.at[i, 'explanation'] = f'Error: {str(e)}'
            df.at[i, 'evidence_phrases'] = ''
    
    # Save results
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
    print(f"Processed {len(df)} reviews with {len(df[df['predicted_label'] == 'Error'])} errors")
    
    return df

if __name__ == "__main__":
    # Test the analyzer
    analyzer = SentimentAnalyzer()
    
    test_review = "This movie was absolutely amazing! Great acting and fantastic storyline."
    result = analyzer.analyze_sentiment(test_review)
    print(json.dumps(result, indent=2))
    
    # Test with empty review
    empty_result = analyzer.analyze_sentiment("")
    print("\nEmpty review test:", json.dumps(empty_result, indent=2))