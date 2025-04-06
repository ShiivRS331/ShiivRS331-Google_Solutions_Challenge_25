import 'package:flutter/material.dart';
import '../utils/constants.dart';

class BottomNavigation extends StatelessWidget {
  final String currentPage;
  final Function(String) onPageChanged;

  const BottomNavigation({
    super.key,
    required this.currentPage,
    required this.onPageChanged,
  });

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double synthButtonSize = screenWidth * 0.20;
    double spacing = screenWidth * 0.12;

    return Align(
      alignment: Alignment.bottomCenter,
      child: Container(
        height: 100,
        decoration: const BoxDecoration(
          color: AppColors.primary,
          borderRadius: BorderRadius.vertical(
            top: Radius.circular(32),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildNavItem('home', currentPage == 'home', Icons.home, const Color(0xFFDBB07B)),
              SizedBox(width: spacing),
              _buildSynthButton(synthButtonSize),
              SizedBox(width: spacing),
              _buildNavItem('upload', currentPage == 'upload', Icons.upload_file, const Color(0xFFDBB07B)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem(String page, bool isActive, IconData icon, Color activeColor) {
    return GestureDetector(
      onTap: () => onPageChanged(page),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: isActive ? activeColor : const Color(0xFFDBB07B), size: 28),
          const SizedBox(height: 8),
          if (isActive)
            Container(
              width: 3,
              height: 3,
              decoration: BoxDecoration(
                color: activeColor,
                shape: BoxShape.circle,
              ),
            )
          else
            Text(
              page,
              style: TextStyle(
                color: activeColor,
                fontSize: 10,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildSynthButton(double size) {
    return GestureDetector(
      onTap: () => onPageChanged('synth'),
      child: Container(
        width: size,
        height: size,
        decoration: const BoxDecoration(
          color: AppColors.accent,
          shape: BoxShape.circle,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.graphic_eq, color: AppColors.secondary, size: 29),
            const SizedBox(height: 8),
            const Text(
              'synth',
              style: TextStyle(
                color: AppColors.secondary,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
