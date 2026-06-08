import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum UserRole { teacher, student }

class AuthProvider extends ChangeNotifier {
  String? _token;
  UserRole? _role;
  bool _isAuthenticated = false;

  bool get isAuthenticated => _isAuthenticated;
  String? get token => _token;
  UserRole? get role => _role;

  Future<void> login(String token, String roleStr) async {
    _token = token;
    _role = roleStr.toUpperCase() == 'TEACHER' ? UserRole.teacher : UserRole.student;
    _isAuthenticated = true;
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
    await prefs.setString('user_role', roleStr);
    
    notifyListeners();
  }

  Future<void> logout() async {
    _token = null;
    _role = null;
    _isAuthenticated = false;
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    
    notifyListeners();
  }

  Future<void> checkLocalAuth() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    final roleStr = prefs.getString('user_role');
    
    if (token != null && roleStr != null) {
      _token = token;
      _role = roleStr.toUpperCase() == 'TEACHER' ? UserRole.teacher : UserRole.student;
      _isAuthenticated = true;
      notifyListeners();
    }
  }
}
