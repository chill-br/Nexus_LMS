import 'dart:io';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LMSService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'https://ais-dev-lnfaqptfayxdph2mlujdm5-347342100546.asia-southeast1.run.app', 
    connectTimeout: const Duration(seconds: 5),
    receiveTimeout: const Duration(seconds: 3),
  ));

  // Singleton pattern
  static final LMSService _instance = LMSService._internal();
  factory LMSService() => _instance;
  LMSService._internal() {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final prefs = await SharedPreferences.getInstance();
        final token = prefs.getString('access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
    ));
  }

  /// Handles Login and stores JWT
  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await _dio.post('/api/users/login/', data: {
        'username': username,
        'password': password,
      });
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', response.data['access']);
      await prefs.setString('refresh_token', response.data['refresh']);
      
      return response.data;
    } on DioException catch (e) {
      throw Exception('Login failed: ${e.message}');
    }
  }

  /// Submits an assignment with a PDF file
  Future<void> submitAssignment({
    required int taskId,
    required File file,
  }) async {
    try {
      String fileName = file.path.split('/').last;
      FormData formData = FormData.fromMap({
        "task": taskId,
        "file": await MultipartFile.fromFile(file.path, filename: fileName),
      });

      await _dio.post('/api/assignments/submit/', data: formData);
    } on DioException catch (e) {
      throw Exception('Submission failed: ${e.message}');
    }
  }

  /// Handles Registration
  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String password,
    required String role,
  }) async {
    try {
      final response = await _dio.post('/api/users/register/', data: {
        'username': username,
        'email': email,
        'password': password,
        'role': role,
      });
      return response.data;
    } on DioException catch (e) {
      throw Exception('Registration failed: ${e.message}');
    }
  }

  /// Refreshes the JWT token
  Future<void> refreshToken() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final refresh = prefs.getString('refresh_token');
      if (refresh == null) return;

      final response = await _dio.post('/api/users/token/refresh/', data: {
        'refresh': refresh,
      });
      
      await prefs.setString('access_token', response.data['access']);
    } on DioException catch (e) {
      throw Exception('Token refresh failed');
    }
  }

  /// Fetches the stream posts for a specific course
  Future<List<dynamic>> getPosts(int courseId) async {
    try {
      final response = await _dio.get('/api/classroom/posts/', queryParameters: {
        'course_id': courseId,
      });
      return response.data;
    } on DioException catch (e) {
      throw Exception('Failed to fetch posts: ${e.message}');
    }
  }

  /// Uploads a PDF as course material and triggers AI indexing
  Future<void> uploadCourseMaterial({
    required int courseId,
    required File file,
  }) async {
    try {
      String fileName = file.path.split('/').last;
      FormData formData = FormData.fromMap({
        "course": courseId,
        "file": await MultipartFile.fromFile(file.path, filename: fileName),
      });

      await _dio.post('/api/classroom/upload-material/', data: formData);
    } on DioException catch (e) {
      throw Exception('Upload failed: ${e.message}');
    }
  }

  /// Sends a question to the RAG AI bot (using the /chat endpoint)
  Future<String> askAI(String query, String courseId) async {
    try {
      final response = await _dio.post('/api/ai/chat/', data: {
        'query': query,
        'course_id': courseId,
      });
      return response.data['answer'];
    } on DioException catch (e) {
      throw Exception('AI Chat failed: ${e.message}');
    }
  }
}
