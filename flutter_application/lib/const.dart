class AppConstants {
  // Base URL for your Flask backend
  static const String baseUrl = "http://127.0.0.1:5500"; // Change this to your server's IP and port if needed

  // API endpoints
  static const String sendOtpEndpoint = "/send_otp";
  static const String validateOtpEndpoint = "/validate_otp";

  // Button texts
  static const String sendOtpButton = "Send OTP";
  static const String validateOtpButton = "Validate OTP";

  // Success messages
  static const String otpSentSuccess = "OTP sent successfully!";
  static const String otpValidationSuccess = "OTP validated successfully!";

  // Label text
  static const String otpLabel = "Enter OTP";
}
