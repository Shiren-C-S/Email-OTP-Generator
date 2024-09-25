import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:dartz/dartz.dart';

class HttpHandler {
  final String baseUrl;

  HttpHandler(this.baseUrl);

  Future<Either<http.Response, String>> postRequest(String endpoint, Map<String, dynamic> body) async {
    try {
      final url = Uri.parse('$baseUrl$endpoint');
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        return Left(response);
      } else {
        return Right('Error: ${response.statusCode}, ${jsonDecode(response.body)["error"]}');
      }
    } catch (e) {
      return Right('Exception: $e');
    }
  }
}
