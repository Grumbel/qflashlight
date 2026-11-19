// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#include "application.hpp"

#include <QApplication>
#include <QCommandLineParser>
#include <QCommandLineOption>
#include <QColor>
#include <QFont>
#include <QRect>
#include <QRegularExpression>
#include <QFile>
#include <QTextStream>
#include <QDebug>
#include <cstdlib>
#include <optional>

static QRect parseGeometry(const QString& text)
{
  static const QRegularExpression re(R"(^(\d+)x(\d+)\+(\d+)\+(\d+)$)");
  const auto m = re.match(text);
  if (!m.hasMatch()) {
    qCritical() << "error: couldn't parse geometry (WxH+X+Y):" << text;
    std::exit(1);
  }
  return QRect(m.captured(3).toInt(), m.captured(4).toInt(),
               m.captured(1).toInt(), m.captured(2).toInt());
}

static QColor parseColor(const QString& text)
{
  QColor c(text);
  if (!c.isValid()) {
    qCritical() << "invalid color name:" << text;
    std::exit(1);
  }
  return c;
}

int main(int argc, char* argv[])
{
  QApplication qapp(argc, argv);
  QApplication::setApplicationName("qflashlight");
  QApplication::setApplicationVersion("0.3.0");
  QApplication::setOrganizationName("grumbel");
  QApplication::setDesktopFileName("qflashlight");

  QCommandLineParser parser;
  parser.setApplicationDescription(QApplication::tr(
    "QFlashlight - Fill the screen with a solid color"));
  parser.addHelpOption();
  parser.addVersionOption();
  parser.addPositionalArgument("FILE", QApplication::tr("Optional text file (or - for stdin)"), "[FILE]");

  // Style
  QCommandLineOption colorOpt({"c", "color"},
    QApplication::tr("Color to use for the background (#FFF, #FFFFFF or name)"),
    "COLOR", "black");
  parser.addOption(colorOpt);

  QCommandLineOption textColorOpt({"T", "text-color"},
    QApplication::tr("Color to use for text"), "COLOR", "white");
  parser.addOption(textColorOpt);

  QCommandLineOption fontOpt({"F", "font"},
    QApplication::tr("Use FONT to display text"), "FONT");
  parser.addOption(fontOpt);

  // Content
  QCommandLineOption textOpt({"t", "text"},
    QApplication::tr("Display text"), "TEXT");
  parser.addOption(textOpt);

  QCommandLineOption commandOpt({"C", "command"},
    QApplication::tr("Runs CMD and shows the output"), "CMD");
  parser.addOption(commandOpt);

  QCommandLineOption intervalOpt({"n", "interval"},
    QApplication::tr("Refresh the screen and rerun command every SECONDS seconds"),
    "SECONDS");
  parser.addOption(intervalOpt);

  // Window
  QCommandLineOption fullscreenOpt({"f", "fullscreen"},
    QApplication::tr("Start in fullscreen mode"));
  parser.addOption(fullscreenOpt);

  QCommandLineOption windowOpt({"w", "window"},
    QApplication::tr("Start in window mode (default)"));
  parser.addOption(windowOpt);

  QCommandLineOption hideCursorOpt({"m", "hide-cursor"},
    QApplication::tr("Hide the mouse cursor"));
  parser.addOption(hideCursorOpt);

  QCommandLineOption borderlessOpt({"b", "borderless"},
    QApplication::tr("Run the window without a border"));
  parser.addOption(borderlessOpt);

  QCommandLineOption geometryOpt({"g", "geometry"},
    QApplication::tr("Set the size and position of the window"), "WxH+X+Y");
  parser.addOption(geometryOpt);

  parser.process(qapp);

  Application app;

  // Style
  app.setBackgroundColor(parseColor(parser.value(colorOpt)));
  app.setForegroundColor(parseColor(parser.value(textColorOpt)));
  if (parser.isSet(fontOpt)) {
    app.setFont(QFont(parser.value(fontOpt)));
  }

  // Content: FILE / -t / -C
  const QStringList pos = parser.positionalArguments();
  if (!pos.isEmpty()) {
    const QString file = pos.first();
    QString text;
    if (file == "-") {
      QTextStream in(stdin);
      text = in.readAll();
    } else {
      QFile f(file);
      if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qCritical() << "cannot open" << file << ":" << f.errorString();
        return 1;
      }
      text = QString::fromLocal8Bit(f.readAll());
    }
    if (text.endsWith('\n')) {
      text.chop(1);
    }
    app.setText(text);
  } else if (parser.isSet(textOpt)) {
    app.setText(parser.value(textOpt));
  }

  if (parser.isSet(commandOpt)) {
    std::optional<double> interval;
    if (parser.isSet(intervalOpt)) {
      bool ok = false;
      const double v = parser.value(intervalOpt).toDouble(&ok);
      if (ok) {
        interval = v;
      }
    }
    app.setCommand(parser.value(commandOpt), interval);
  }

  // Window
  // Default is window mode (matches current Python: -w is default, -f for fullscreen)
  if (parser.isSet(fullscreenOpt)) {
    app.setFullscreen(true);
  }
  if (parser.isSet(borderlessOpt)) {
    app.setBorderless(true);
  }
  if (parser.isSet(hideCursorOpt)) {
    app.setCursorVisible(false);
  }
  if (parser.isSet(geometryOpt)) {
    app.setWindowGeometry(parseGeometry(parser.value(geometryOpt)));
  }

  app.show();
  return qapp.exec();
}
