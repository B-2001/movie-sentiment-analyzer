import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def analyze_results():
    # Load the results
    df = pd.read_csv('results.csv')
    
    # Calculate accuracy
    accuracy = accuracy_score(df['true_sentiment'], df['predicted_label'])
    
    # Generate classification report
    report = classification_report(df['true_sentiment'], df['predicted_label'])
    
    # Generate confusion matrix
    cm = confusion_matrix(df['true_sentiment'], df['predicted_label'])
    
    print("=== PERFORMANCE METRICS ===")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Number of reviews: {len(df)}")
    print(f"Positive reviews: {sum(df['true_sentiment'] == 'Positive')}")
    print(f"Negative reviews: {sum(df['true_sentiment'] == 'Negative')}")
    print(f"Neutral reviews: {sum(df['true_sentiment'] == 'Neutral')}")
    
    print("\n=== CLASSIFICATION REPORT ===")
    print(report)
    
    print("=== CONFUSION MATRIX ===")
    print("Rows: Actual, Columns: Predicted")
    print(cm)
    
    # Calculate per-class accuracy
    correct = df['true_sentiment'] == df['predicted_label']
    print("\n=== PER-CLASS ACCURACY ===")
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        class_data = df[df['true_sentiment'] == sentiment]
        class_accuracy = accuracy_score(class_data['true_sentiment'], class_data['predicted_label'])
        print(f"{sentiment}: {class_accuracy:.2%} ({sum(class_data['true_sentiment'] == class_data['predicted_label'])}/{len(class_data)})")
    
    # Calculate average confidence
    print(f"\n=== AVERAGE CONFIDENCE ===")
    print(f"Overall: {df['confidence_score'].mean():.2f}")
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        avg_conf = df[df['predicted_label'] == sentiment]['confidence_score'].mean()
        print(f"{sentiment}: {avg_conf:.2f}")

if __name__ == "__main__":
    analyze_results()