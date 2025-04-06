import 'package:flutter/material.dart';
import '../utils/constants.dart';
import '../widgets/bottom_navigation.dart';

class SynthScreen extends StatelessWidget {
  final Function(String) onPageChanged;
  final bool isFullScreen;
  final VoidCallback onToggleFullScreen;

  const SynthScreen({
    super.key,
    required this.onPageChanged,
    required this.isFullScreen,
    required this.onToggleFullScreen,
  });

  @override
  Widget build(BuildContext context) {
    if (isFullScreen) {
      return _buildFullScreenView();
    }
    return _buildNormalView();
  }

  Widget _buildFullScreenView() {
    return Container(
      color: Colors.black,
      child: Stack(
        children: [
          Center(
            child: Text(
              'the graph\n(full screen)\npinch to zoom',
              style: AppTextStyles.heading.copyWith(fontSize: 24),
              textAlign: TextAlign.center,
            ),
          ),
          Positioned(
            top: 30,
            right: 25,
            child: GestureDetector(
              onTap: onToggleFullScreen,
              child: const Icon(
                Icons.close,
                color: AppColors.accent,
                size: 32,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNormalView() {
    return Container(
      decoration: const BoxDecoration(
        color: AppColors.secondary,
        borderRadius: BorderRadius.all(Radius.circular(36)),
      ),
      child: Stack(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(25, 50, 25, 134),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.black,
                borderRadius: BorderRadius.circular(37),
              ),
              child: Stack(
                children: [
                  Center(
                    child: Text(
                      'the graph',
                      style: AppTextStyles.heading.copyWith(fontSize: 20),
                    ),
                  ),
                  Positioned(
                    top: 30,
                    right: 25,
                    child: GestureDetector(
                      onTap: onToggleFullScreen,
                      child: const Icon(
                        Icons.fullscreen,
                        color: AppColors.accent,
                        size: 32,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: BottomNavigation(
              currentPage: 'synth',
              onPageChanged: onPageChanged,
            ),
          ),
        ],
      ),
    );
  }
}