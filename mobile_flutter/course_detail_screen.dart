import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'classroom_ui.dart';
import 'lms_service.dart';
import 'auth_provider.dart';

class CourseDetailScreen extends StatefulWidget {
  final int courseId;
  final String courseName;

  const CourseDetailScreen({super.key, required this.courseId, required this.courseName});

  @override
  State<CourseDetailScreen> createState() => _CourseDetailScreenState();
}

class _CourseDetailScreenState extends State<CourseDetailScreen> {
  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final isTeacher = auth.role == UserRole.teacher;
    
    return DefaultTabController(
      length: isTeacher ? 4 : 3,
      child: Scaffold(
        appBar: AppBar(
          title: Text(widget.courseName),
          backgroundColor: Colors.white,
          foregroundColor: Colors.grey[800],
          elevation: 1,
          bottom: TabBar(
            labelColor: Colors.indigo,
            unselectedLabelColor: Colors.grey,
            indicatorColor: Colors.indigo,
            isScrollable: false,
            tabs: [
              const Tab(text: "Stream"),
              const Tab(text: "Classwork"),
              const Tab(text: "People"),
              if (isTeacher) const Tab(text: "Grades"),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            StreamScreen(courseId: widget.courseId),
            ClassworkScreen(courseId: widget.courseId),
            PeopleScreen(courseId: widget.courseId),
            if (isTeacher) GradesScreen(courseId: widget.courseId),
          ],
        ),
      ),
    );
  }
}

class StreamScreen extends StatelessWidget {
  final int courseId;
  const StreamScreen({super.key, required this.courseId});
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<dynamic>>(
      future: LMSService().getPosts(courseId),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
        if (snapshot.hasError) return Center(child: Text("Error: ${snapshot.error}"));
        final posts = snapshot.data ?? [];
        
        if (posts.isEmpty) {
          return const Center(child: Text("No announcements yet."));
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: posts.length,
          itemBuilder: (context, index) {
            final post = posts[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: ListTile(
                leading: CircleAvatar(child: Text(post['author_name'][0])),
                title: Text(post['author_name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text(post['content']),
                trailing: Text(post['created_at'].toString().substring(5, 10)),
              ),
            );
          },
        );
      }
    );
  }
}

class ClassworkScreen extends StatelessWidget {
  final int courseId;
  const ClassworkScreen({super.key, required this.courseId});
  
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ListTile(
          leading: const CircleAvatar(backgroundColor: Colors.indigo, child: Icon(Icons.assignment, color: Colors.white)),
          title: const Text("Lab 4: Entanglement Simulation"),
          subtitle: const Text("Due: Tomorrow"),
          onTap: () {},
        ),
        const Divider(),
        ListTile(
          leading: const CircleAvatar(backgroundColor: Colors.indigo, child: Icon(Icons.assignment, color: Colors.white)),
          title: const Text("Neural Networks Deep Dive"),
          subtitle: const Text("Due: Next Week"),
          onTap: () {},
        ),
      ],
    );
  }
}

class PeopleScreen extends StatelessWidget {
  final int courseId;
  const PeopleScreen({super.key, required this.courseId});

  @override
  Widget build(BuildContext context) {
    return const Center(child: Text("List of Teachers & Enrolled Students"));
  }
}

class GradesScreen extends StatelessWidget {
  final int courseId;
  const GradesScreen({super.key, required this.courseId});

  @override
  Widget build(BuildContext context) {
    return const Center(child: Text("Teacher View: Student Grades Table"));
  }
}
