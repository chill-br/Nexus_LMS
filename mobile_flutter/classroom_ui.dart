import 'package:flutter/material.dart';
import 'lms_service.dart';

class ClassroomStreamPage extends StatefulWidget {
  final int courseId;
  final String courseName;

  const ClassroomStreamPage({super.key, required this.courseId, required this.courseName});

  @override
  State<ClassroomStreamPage> createState() => _ClassroomStreamPageState();
}

class _ClassroomStreamPageState extends State<ClassroomStreamPage> {
  final List<dynamic> _posts = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchPosts();
  }

  Future<void> _fetchPosts() async {
    try {
      final posts = await LMSService().getPosts(widget.courseId);
      setState(() {
        _posts.addAll(posts);
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.courseName),
        backgroundColor: Colors.indigo[600],
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : ListView.builder(
            itemCount: _posts.length,
            itemBuilder: (context, index) {
              final post = _posts[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          CircleAvatar(child: Text(post['author_name'][0].toUpperCase())),
                          const SizedBox(width: 12),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(post['author_name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                              Text(post['created_at'].toString().substring(0, 10), style: const TextStyle(color: Colors.grey, fontSize: 12)),
                            ],
                          )
                        ],
                      ),
                      const SizedBox(height: 12),
                      Text(post['content']),
                    ],
                  ),
                ),
              );
            },
          ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showJoinClassDialog(context),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _showJoinClassDialog(BuildContext context) {
    final TextEditingController codeController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Join Class"),
        content: TextField(
          controller: codeController,
          decoration: const InputDecoration(hintText: "Enter 6-digit class code"),
          maxLength: 6,
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () async {
              try {
                // Call DJango Join endpoint via LMSService (to be added)
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Joining...")));
              } catch (e) {
                print(e);
              }
            }, 
            child: const Text("Join")
          ),
        ],
      ),
    );
  }
}
