import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'screens/home_screen.dart';
import 'screens/synth_screen.dart';
import 'screens/upload_screen.dart';
import 'widgets/profile_modal.dart';
import 'utils/constants.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shruti',
      theme: ThemeData(
        textTheme: GoogleFonts.interTextTheme(),
        primaryColor: AppColors.primary,
        scaffoldBackgroundColor: AppColors.background,
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});
  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  String currentPage = 'home';
  bool isFullScreen = false;
  bool showProfileModal = false;
  bool isLoggedIn = false;
  String userEmail = '';
  String userImage = 'https://placehold.co/45x45';

  void navigateTo(String page) {
    setState(() {
      currentPage = page;
      if (page != 'synth') {
        isFullScreen = false;
      }
    });
  }

  void toggleFullScreen() {
    setState(() {
      isFullScreen = !isFullScreen;
    });
  }

  void toggleProfile() {
    setState(() {
      showProfileModal = !showProfileModal;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Center(
            child: SizedBox(
              width: 390,
              height: 844,
              child: _buildCurrentScreen(),
            ),
          ),
          if (showProfileModal)
            ProfileModal(
              isLoggedIn: isLoggedIn,
              userEmail: userEmail,
              userImage: userImage,
              onClose: toggleProfile,
              onSignIn: () {
                setState(() {
                  isLoggedIn = true;
                  showProfileModal = false;
                });
              },
              onSignOut: () {
                setState(() {
                  isLoggedIn = false;
                  showProfileModal = false;
                });
              },
              onContinueAsGuest: () {
                setState(() {
                  showProfileModal = false;
                });
              },
            ),
        ],
      ),
    );
  }

  Widget _buildCurrentScreen() {
    switch (currentPage) {
      case 'home':
        return HomeScreen(
          onPageChanged: navigateTo,
          onProfileTap: toggleProfile,
          userImage: userImage,
        );
      case 'synth':
        return SynthScreen(
          onPageChanged: navigateTo,
          isFullScreen: isFullScreen,
          onToggleFullScreen: toggleFullScreen,
        );
      case 'upload':
        return UploadScreen(
          onPageChanged: navigateTo,
          onProfileTap: toggleProfile,
          userImage: userImage,
        );
      case 'graph':
        return GraphScreen();
      default:
        return const SizedBox.shrink();
    }
  }
}

class GraphScreen extends StatefulWidget {
  @override
  _GraphScreenState createState() => _GraphScreenState();
}

class _GraphScreenState extends State<GraphScreen> {
  late WebSocketChannel channel;
  String note = 'Connecting...';
  String octave = '';
  double frequency = 0.0;
  Uint8List? imageBytes;

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
  }

  void _connectWebSocket() {
    try {
      channel = WebSocketChannel.connect(Uri.parse('ws://10.0.2.2:65431'));
      channel.stream.listen((message) {
        print("Received message: $message");
        try {
          final data = json.decode(message);
          print("Parsed data: $data");
          setState(() {
            note = data['note'] ?? 'N/A';
            octave = data['octave'] ?? '';
            frequency = data['frequency'] ?? 0.0;
          });
        } catch (e) {
          print('Error decoding JSON: $e');
          setState(() {
            note = 'Error';
          });
        }
      }, onError: (error) {
        print('WebSocket error: $error');
        setState(() {
          note = 'Error connecting';
        });
      }, onDone: () {
        print('WebSocket connection closed');
        setState(() {
          note = 'Connection closed';
        });
      });
    } catch (e) {
      print('Error connecting to WebSocket: $e');
      setState(() {
        note = 'Error connecting';
      });
    }
  }

  @override
  void dispose() {
    channel.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Note Graph')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('Note: $note ($octave)'),
            Text('Frequency: ${frequency.toStringAsFixed(2)} Hz'),

          ],
        ),
      ),
    );
  }
}

