import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppColors {
  static const Color primary = Color(0xFF992108);
  static const Color secondary = Color(0xFF4D040F);
  static const Color accent = Color(0xFFDBB07B);
  static const Color background = Color(0xFF111111);
  static const Color white = Color(0xFFFFFFFF);
  static const Color textGrey = Color(0xFF5F6368);
  static const Color borderGrey = Color(0xFFDADCE0);
  static const Color textDark = Color(0xFF202124);
}

class AppTextStyles {
  static TextStyle get logo => GoogleFonts.inter(
    fontSize: 48,
    color: AppColors.accent,
    letterSpacing: -1.34,
  );

  static TextStyle get heading => GoogleFonts.inter(
    fontSize: 48,
    color: AppColors.accent,
    letterSpacing: -1.34,
  );

  static TextStyle get subheading => GoogleFonts.inter(
    fontSize: 24,
    color: Colors.white,
    letterSpacing: -1.34,
  );

  static TextStyle get body => GoogleFonts.inter(
    fontSize: 14,
    color: AppColors.textGrey,
  );

  static TextStyle get button => GoogleFonts.inter(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    color: AppColors.textDark,
  );
}

class AppDimensions {
  static const double screenPadding = 24.0;
  static const double borderRadius = 36.0;
  static const double buttonHeight = 48.0;
  static const double iconSize = 32.0;
}