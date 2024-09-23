import 'package:email_otp/email_otp.dart';
import 'package:flutter/material.dart';

void main() {
  EmailOTP.config(
    appName: 'OTP_Generator',
    otpType: OTPType.numeric,
    emailTheme: EmailTheme.v5,
  );
    EmailOTP.setSMTP(
    host: 'smtp.gmail.com',
    emailPort: EmailPort.port587, // TLS
    secureType: SecureType.tls,
    username: 'drshiran2003@gmail.com',
    password: 'qshn nwjj yvex inhk', 
  );

  runApp(const MaterialApp(
    debugShowCheckedModeBanner: false,
    home: HomePage(),
  ));
}


class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController otpController = TextEditingController();
  bool isLoading = false;
  bool isOtpSent = false;

  Future<void> sendOtp() async {
    setState(() {
      isLoading = true;
    });
    bool result = await EmailOTP.sendOTP(email: emailController.text);
    setState(() {
      isLoading = false;
      isOtpSent = result;
    });
    if (result) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("OTP has been sent")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to send OTP")),
      );
    }
  }

  Future<void> verifyOtp() async {
    setState(() {
      isLoading = true;
    });
    bool result = await EmailOTP.verifyOTP(otp: otpController.text);
    setState(() {
      isLoading = false;
    });
    if (result) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("OTP verified successfully")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Invalid OTP")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        title: const Text('OTP Verification'),
        centerTitle: true,
        backgroundColor: Colors.blueGrey,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Enter your email to receive an OTP:',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: emailController,
              decoration: InputDecoration(
                labelText: 'Email Address',
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10.0),
                ),
                prefixIcon: const Icon(Icons.email),
              ),
              keyboardType: TextInputType.emailAddress,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: isLoading ? null : sendOtp,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 15),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0),
                ),
                backgroundColor: Colors.blueGrey,
              ),
              child: isLoading
                  ? const CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    )
                  : const Text(
                      'Send OTP',
                      style: TextStyle(fontSize: 18),
                    ),
            ),
            const SizedBox(height: 30),
            if (isOtpSent) ...[
              const Text(
                'Enter the OTP sent to your email:',
                style: TextStyle(fontSize: 18),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: otpController,
                decoration: InputDecoration(
                  labelText: 'Enter OTP',
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                  prefixIcon: const Icon(Icons.lock),
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: isLoading ? null : verifyOtp,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 15),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                  backgroundColor: Colors.blueGrey,
                ),
                child: isLoading
                    ? const CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      )
                    : const Text(
                        'Verify OTP',
                        style: TextStyle(fontSize: 18),
                      ),
              ),
            ]
          ],
        ),
      ),
    );
  }
}
