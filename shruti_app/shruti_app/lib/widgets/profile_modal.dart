import 'package:flutter/material.dart';
import '../utils/constants.dart';

class ProfileModal extends StatelessWidget {
  final bool isLoggedIn;
  final String? userEmail;
  final String? userImage;
  final VoidCallback onClose;
  final VoidCallback onSignIn;
  final VoidCallback onSignOut;
  final VoidCallback onContinueAsGuest;

  const ProfileModal({
    super.key,
    required this.isLoggedIn,
    this.userEmail,
    this.userImage,
    required this.onClose,
    required this.onSignIn,
    required this.onSignOut,
    required this.onContinueAsGuest,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black.withOpacity(0.5),
      child: Center(
        child: SingleChildScrollView(
          child: Container(
            margin: const EdgeInsets.only(top: 80),
            width: 360,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildHeader(),
                _buildContent(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: const BoxDecoration(
        border: Border(
          bottom: BorderSide(
            color: AppColors.borderGrey,
            width: 1,
          ),
        ),
      ),
      child: Stack(
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min, // Added MainAxisSize.min
            children: [
              Text(
                'Sign in with Google',
                style: AppTextStyles.heading.copyWith(
                  fontSize: 20,
                  color: AppColors.textDark,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'to continue to shruti',
                style: AppTextStyles.body,
              ),
            ],
          ),
          Positioned(
            right: 0,
            top: 0,
            child: IconButton(
              constraints: const BoxConstraints(), //added this line.
              visualDensity: VisualDensity.compact, // added this line.
              onPressed: onClose,
              icon: const Icon(Icons.close),
              color: AppColors.textGrey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildContent() {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: isLoggedIn ? _buildLoggedInContent() : _buildSignInContent(),
    );
  }

  Widget _buildSignInContent() {
    return Column(
      children: [
        _buildAuthButton(
          'Sign in with Google',
          'assets/google_icon.png',
          onSignIn,
        ),
        const SizedBox(height: 16),
        _buildAuthButton(
          'Continue as guest',
          'assets/guest_icon.png',
          onContinueAsGuest,
        ),
      ],
    );
  }

  Widget _buildLoggedInContent() {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            border: Border.all(color: AppColors.borderGrey),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            children: [
              CircleAvatar(
                radius: 20,
                backgroundImage: NetworkImage(userImage ?? ''),
                onBackgroundImageError: (exception, stackTrace) {
                  print('Error loading user image: $exception');
                },
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      userEmail ?? '',
                      style: AppTextStyles.button,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      'Google Account',
                      style: AppTextStyles.body.copyWith(fontSize: 12),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        SizedBox(
          width: double.infinity,
          height: 36,
          child: ElevatedButton(
            onPressed: onSignOut,
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF1A73E8),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18),
              ),
            ),
            child: Text(
              'Sign out',
              style: AppTextStyles.button.copyWith(color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAuthButton(String text, String iconPath, VoidCallback onTap) {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: OutlinedButton(
        onPressed: onTap,
        style: OutlinedButton.styleFrom(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
          side: const BorderSide(color: AppColors.borderGrey),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              iconPath,
              width: 18,
              height: 18,
              errorBuilder: (context, error, stackTrace) {
                print('Error loading asset image: $error');
                return const Icon(Icons.error);
              },
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                text,
                style: AppTextStyles.button,
                overflow: TextOverflow.ellipsis,
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }
}