import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'auth_provider.dart';
import 'login_screen.dart';
import 'classroom_ui.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final authProvider = AuthProvider();
  await authProvider.checkLocalAuth();
  
  runApp(
    ChangeNotifierProvider(
      create: (_) => authProvider,
      child: const LMSApp(),
    ),
  );
}

class LMSApp extends StatelessWidget {
  const LMSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nexus Classroom',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.indigo,
          primary: Colors.indigo[600],
        ),
        fontFamily: 'Roboto',
      ),
      home: const AuthWrapper(),
    );
  }
}

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    
    if (auth.isAuthenticated) {
      // In a real app, this would be a HomeScreen listing the courses
      // For now, redirecting to a placeholder "My Classes" view
      return const MyClassesScreen();
    }
    
    return const LoginScreen();
  }
}

class MyClassesScreen extends StatefulWidget {
  const MyClassesScreen({super.key});

  @override
  State<MyClassesScreen> createState() => _MyClassesScreenState();
}

class _MyClassesScreenState extends State<MyClassesScreen> {
  final _nameController = TextEditingController();
  final _codeController = TextEditingController();
  bool _isLoading = false;

  void _showCreateCourseDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Create Course"),
        content: TextField(
          controller: _nameController,
          decoration: const InputDecoration(labelText: "Course Name", hintText: "e.g. Quantum Physics"),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () async {
              // Perform API call to create course
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Course created successfully!")));
            },
            child: const Text("Create"),
          ),
        ],
      ),
    );
  }

  void _showJoinCourseDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Join Course"),
        content: TextField(
          controller: _codeController,
          decoration: const InputDecoration(labelText: "6-Digit Code", hintText: "e.g. A7B2X9"),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () async {
              // Perform API call to join course
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Joined course successfully!")));
            },
            child: const Text("Join"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final isTeacher = auth.role == UserRole.teacher;
    
    return Scaffold(
      appBar: AppBar(
        title: const Text("Nexus Classroom"),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => auth.logout(),
          )
        ],
      ),
      body: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.dashboard_customize, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text("No classes here yet.", style: TextStyle(fontSize: 18, color: Colors.grey)),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: isTeacher ? _showCreateCourseDialog : _showJoinCourseDialog,
        label: Text(isTeacher ? "Create Class" : "Join Class"),
        icon: const Icon(Icons.add),
      ),
    );
  }
}
