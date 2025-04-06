import 'package:flutter/material.dart';
import '../utils/constants.dart';
import '../models/song.dart';
import '../widgets/bottom_navigation.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';

class HomeScreen extends StatefulWidget {
  final Function(String) onPageChanged;
  final VoidCallback onProfileTap;
  final String userImage;

  const HomeScreen({
    super.key,
    required this.onPageChanged,
    required this.onProfileTap,
    required this.userImage,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String searchQuery = '';
  Uint8List? _graphImageBytes;
  String _note = 'None';
  String _octave = 'None';
  double _frequency = 0.0;
  late WebSocketChannel _channel;
  bool _isFullScreen = false;

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
  }

  @override
  void dispose() {
    _channel.sink.close();
    super.dispose();
  }

  void _connectWebSocket() {
    try {
      _channel = WebSocketChannel.connect(Uri.parse('ws://10.0.2.2:65431'));
      _channel.stream.listen((message) {
        try {
          final data = json.decode(message);
          setState(() {
            _note = data['note'] ?? 'N/A';
            _octave = data['octave'] ?? '';
            _frequency = data['frequency'] ?? 0.0;
            if (data['image'] != null) {
              _graphImageBytes = base64.decode(data['image']);
            }
          });
        } catch (e) {
          print('Error decoding JSON: $e');
        }
      }, onError: (error) {
        print('WebSocket error: $error');
      }, onDone: () {
        print('WebSocket connection closed');
      });
    } catch (e) {
      print('Error connecting to WebSocket: $e');
    }
  }

  void _toggleFullScreen() {
    setState(() {
      _isFullScreen = !_isFullScreen;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF992108),
      body: Stack(
        children: [
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            height: 540,
            child: Container(
              decoration: const BoxDecoration(
                color: Color(0xFF4D040F),
                borderRadius: BorderRadius.all(Radius.circular(37)),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 40),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.only(top: 30, right: 25),
                  child: Align(
                    alignment: Alignment.topRight,
                    child: GestureDetector(
                      onTap: widget.onProfileTap,
                      child: CircleAvatar(
                        radius: 22.5,
                        backgroundImage: NetworkImage(widget.userImage),
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(left: 20, top: 1),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                    child: Text(
                      'shruti',
                      style: AppTextStyles.logo,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(top: 30),
                  child: Row(
                    children: [
                      Expanded(
                        child: Container(
                          height: 45,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(9),
                            border: Border.all(color: Colors.white),
                          ),
                          child: TextField(
                            onChanged: (value) => setState(() => searchQuery = value),
                            decoration: const InputDecoration(
                              hintText: 'search song',
                              hintStyle: TextStyle(color: Color(0xFFDBB07B)),
                              contentPadding: EdgeInsets.symmetric(horizontal: 15),
                              border: InputBorder.none,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 15),
                      Container(
                        width: 45,
                        height: 45,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(7),
                          border: Border.all(color: Colors.white),
                        ),
                        child: const Icon(
                          Icons.search,
                          color: Color(0xFF4D040F),
                          size: 28,
                        ),
                      ),
                    ],
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(top: 25),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: const Text(
                      'Hello, Aksh',
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFDBB07B),
                        fontFamily: 'Inter',
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 15),
                Expanded(
                  child: GestureDetector(
                    onTap: _toggleFullScreen,
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      decoration: BoxDecoration(
                        color: const Color(0xFF4D040F),
                        borderRadius: BorderRadius.circular(15),
                      ),
                      padding: const EdgeInsets.all(12),
                      child: Stack(
                        children: [
                          Container(
                            decoration: BoxDecoration(
                              color: Colors.black,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Center(
                              child: Text(
                                'the graph\nreal time audio',
                                textAlign: TextAlign.center,
                                style: TextStyle(color: Color(0xFFDBB07B), fontSize: 14),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: BottomNavigation(
              currentPage: 'home',
              onPageChanged: widget.onPageChanged,
            ),
          ),
        ],
      ),
    );
  }
}
