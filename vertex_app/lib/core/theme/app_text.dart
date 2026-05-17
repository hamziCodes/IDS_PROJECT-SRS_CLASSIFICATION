import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppText {
  static TextTheme textTheme = TextTheme(
    displayLarge: GoogleFonts.spaceGrotesk(
      fontSize: 36,
      fontWeight: FontWeight.w600,
      letterSpacing: -0.4,
    ),
    headlineMedium: GoogleFonts.spaceGrotesk(
      fontSize: 24,
      fontWeight: FontWeight.w600,
    ),
    titleLarge: GoogleFonts.spaceGrotesk(
      fontSize: 20,
      fontWeight: FontWeight.w600,
    ),
    titleMedium: GoogleFonts.spaceGrotesk(
      fontSize: 18,
      fontWeight: FontWeight.w600,
    ),
    bodyLarge: GoogleFonts.sora(
      fontSize: 16,
      height: 1.5,
    ),
    bodyMedium: GoogleFonts.sora(
      fontSize: 14,
      height: 1.45,
    ),
    bodySmall: GoogleFonts.sora(
      fontSize: 12,
      height: 1.35,
    ),
    labelLarge: GoogleFonts.sora(
      fontSize: 14,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.2,
    ),
  );
}
