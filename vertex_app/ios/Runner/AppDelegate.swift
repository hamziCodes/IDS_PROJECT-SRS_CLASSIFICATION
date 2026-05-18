import Flutter
import UIKit

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    // Log startup for diagnostics
    NSLog("Vertex: AppDelegate didFinishLaunchingWithOptions")

    GeneratedPluginRegistrant.register(with: self)

    // Catch Objective-C exceptions and log briefly (avoid crashing here)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
