import 'package:flutter/material.dart';
import '../utils/constants.dart';
import '../widgets/bottom_navigation.dart';

class UploadScreen extends StatelessWidget {
  final Function(String) onPageChanged;
  final VoidCallback onProfileTap;
  final String userImage;

  const UploadScreen({
    super.key,
    required this.onPageChanged,
    required this.onProfileTap,
    required this.userImage,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF992108),
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
                      onTap: onProfileTap,
                      child: CircleAvatar(
                        radius: 22.5,
                        backgroundImage: NetworkImage(userImage),
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
                          child: const TextField(
                            decoration: InputDecoration(
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
                    child: Text(
                      'Hello, Aksh',
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFDBB07B),
                        fontFamily: 'Inter',
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 30),
                  child: Container(
                    width: double.infinity,
                    height: 150,
                    decoration: BoxDecoration(
                      color: Color(0xFF4D040F),
                      borderRadius: BorderRadius.circular(25),
                      border: Border.all(color: Color(0xFFDBB07B)),
                    ),
                    child: const Center(
                      child: Text(
                        'upload\n(audio/video/img)',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Color(0xFFDBB07B), fontSize: 18),
                      ),
                    ),
                  ),
                ),
                Column(
                  children: List.generate(
                    4,
                    (index) => Padding(
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      child: Container(
                        width: double.infinity,
                        height: 50,
                        decoration: BoxDecoration(
                          color: Color(0xFFDBB07B),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Center(
                          child: Text(
                            'prompt 1',
                            style: TextStyle(
                              color: Color(0xFF4D040F),
                              fontSize: 18,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
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
              currentPage: 'upload',
              onPageChanged: onPageChanged,
            ),
          ),
        ],
      ),
    );
  }
}