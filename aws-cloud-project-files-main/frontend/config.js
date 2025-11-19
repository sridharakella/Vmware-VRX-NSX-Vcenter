// AWS Configuration
// INSTRUCTIONS: Replace these values with your actual AWS resource IDs after deployment

const AWS_CONFIG = {
    // Cognito Configuration
    region: 'us-east-2', // Change this to your AWS region
    userPoolId: 'us-east-2_lebxkQK3l', // Replace with your Cognito User Pool ID
    userPoolWebClientId: '41o6olto1cikk77q9gg9mh3g70', // Replace with your App Client ID
    
    // API Gateway Configuration
    apiEndpoint: 'https://f2dnk06all.execute-api.us-east-2.amazonaws.com/prod', // Replace with your API Gateway invoke URL (e.g., https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod)
};
//
//

// DO NOT EDIT BELOW THIS LINE
window.AWS_CONFIG = AWS_CONFIG;
