#!/usr/bin/env ruby
# frozen_string_literal: true

require "xcodeproj"
require "fileutils"

ROOT = File.expand_path("..", __dir__)
PROJ_PATH = File.join(ROOT, "FahrPrufungDE.xcodeproj")
UNIT_DIR = File.join(ROOT, "FahrPrufungDETests")
UI_DIR = File.join(ROOT, "FahrPrufungDEUITests")
TEAM = "28QWPQX3PF"
DEPLOYMENT = "17.0"

project = Xcodeproj::Project.open(PROJ_PATH)
app_target = project.targets.find { |t| t.name == "FahrPrufungDE" }
abort "App target FahrPrufungDE not found" unless app_target

# Required for @testable import from unit tests
app_target.build_configurations.each do |config|
  config.build_settings["ENABLE_TESTABILITY"] = "YES" if config.name == "Debug"
end

# Remove existing test targets if re-running
%w[FahrPrufungDETests FahrPrufungDEUITests].each do |name|
  existing = project.targets.find { |t| t.name == name }
  next unless existing
  puts "Removing existing target #{name}"
  existing.remove_from_project
end

# Remove stale product refs / groups
project.main_group.children.each do |child|
  next unless child.respond_to?(:name) || child.respond_to?(:path)
  label = child.respond_to?(:display_name) ? child.display_name : child.path
  if %w[FahrPrufungDETests FahrPrufungDEUITests].include?(label)
    child.remove_from_project
  end
end

def add_sources(target, group, dir)
  Dir.glob(File.join(dir, "**", "*.swift")).sort.each do |path|
    rel = Pathname.new(path).relative_path_from(Pathname.new(File.dirname(dir))).to_s
    # Keep files under the named group with basename only
    ref = group.new_file(path)
    target.add_file_references([ref])
  end
end

unit = project.new_target(:unit_test_bundle, "FahrPrufungDETests", :ios, DEPLOYMENT)
ui = project.new_target(:ui_test_bundle, "FahrPrufungDEUITests", :ios, DEPLOYMENT)

unit_group = project.main_group.new_group("FahrPrufungDETests", "FahrPrufungDETests")
ui_group = project.main_group.new_group("FahrPrufungDEUITests", "FahrPrufungDEUITests")

add_sources(unit, unit_group, UNIT_DIR)
add_sources(ui, ui_group, UI_DIR)

unit.add_dependency(app_target)
ui.add_dependency(app_target)

# Host unit tests in the app so Bundle.main has vocabulary.json / signs.json
unit_attrs = {
  "GENERATE_INFOPLIST_FILE" => "YES",
  "CURRENT_PROJECT_VERSION" => "1",
  "MARKETING_VERSION" => "1.0",
  "PRODUCT_BUNDLE_IDENTIFIER" => "de.fahrprufung.app.tests",
  "PRODUCT_NAME" => "$(TARGET_NAME)",
  "SWIFT_VERSION" => "5.0",
  "TARGETED_DEVICE_FAMILY" => "1",
  "IPHONEOS_DEPLOYMENT_TARGET" => DEPLOYMENT,
  "CODE_SIGN_STYLE" => "Automatic",
  "DEVELOPMENT_TEAM" => TEAM,
  "BUNDLE_LOADER" => "$(TEST_HOST)",
  "TEST_HOST" => "$(BUILT_PRODUCTS_DIR)/FahrPrufungDE.app/$(BUNDLE_EXECUTABLE_FOLDER_PATH)/FahrPrufungDE",
  "LD_RUNPATH_SEARCH_PATHS" => "$(inherited) @executable_path/Frameworks @loader_path/Frameworks"
}

ui_attrs = {
  "GENERATE_INFOPLIST_FILE" => "YES",
  "CURRENT_PROJECT_VERSION" => "1",
  "MARKETING_VERSION" => "1.0",
  "PRODUCT_BUNDLE_IDENTIFIER" => "de.fahrprufung.app.uitests",
  "PRODUCT_NAME" => "$(TARGET_NAME)",
  "SWIFT_VERSION" => "5.0",
  "TARGETED_DEVICE_FAMILY" => "1",
  "IPHONEOS_DEPLOYMENT_TARGET" => DEPLOYMENT,
  "CODE_SIGN_STYLE" => "Automatic",
  "DEVELOPMENT_TEAM" => TEAM,
  "TEST_TARGET_NAME" => "FahrPrufungDE",
  "LD_RUNPATH_SEARCH_PATHS" => "$(inherited) @executable_path/Frameworks @loader_path/Frameworks"
}

[unit, ui].each do |target|
  target.build_configurations.each do |config|
    attrs = target == unit ? unit_attrs : ui_attrs
    attrs.each { |k, v| config.build_settings[k] = v }
  end
end

# Wire Test target membership for UI tests
ui_attributes = project.root_object.attributes["TargetAttributes"] || {}
ui_attributes[ui.uuid] = {
  "TestTargetID" => app_target.uuid,
  "CreatedOnToolsVersion" => "15.0"
}
ui_attributes[unit.uuid] = {
  "TestTargetID" => app_target.uuid,
  "CreatedOnToolsVersion" => "15.0"
}
project.root_object.attributes["TargetAttributes"] = ui_attributes

project.save

# Shared scheme with both testables
scheme_dir = File.join(PROJ_PATH, "xcshareddata", "xcschemes")
FileUtils.mkdir_p(scheme_dir)
scheme = Xcodeproj::XCScheme.new
scheme.configure_with_targets(app_target, nil)
scheme.set_launch_target(app_target)

unit_entry = Xcodeproj::XCScheme::TestAction::TestableReference.new(unit)
ui_entry = Xcodeproj::XCScheme::TestAction::TestableReference.new(ui)
scheme.test_action.add_testable(unit_entry)
scheme.test_action.add_testable(ui_entry)
scheme.test_action.build_configuration = "Debug"
scheme.launch_action.build_configuration = "Debug"
scheme.profile_action.build_configuration = "Release"
scheme.analyze_action.build_configuration = "Debug"
scheme.archive_action.build_configuration = "Release"

scheme.save_as(PROJ_PATH, "FahrPrufungDE", true)

puts "Added targets: FahrPrufungDETests, FahrPrufungDEUITests"
puts "Shared scheme: FahrPrufungDE"
puts "Unit sources: #{unit.source_build_phase.files.count}"
puts "UI sources: #{ui.source_build_phase.files.count}"
