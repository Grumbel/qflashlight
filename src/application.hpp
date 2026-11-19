// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#ifndef QFLASHLIGHT_APPLICATION_HPP
#define QFLASHLIGHT_APPLICATION_HPP

#include <QObject>
#include <QColor>
#include <QFont>
#include <QRect>
#include <QPoint>
#include <QString>
#include <memory>
#include <optional>

class FlashlightModel;
class FlashlightWidget;
class TextGenerator;

class Application : public QObject
{
  Q_OBJECT

public:
  explicit Application(QObject* parent = nullptr);
  ~Application() override;

  FlashlightModel* model() const { return m_model; }

  void show();
  void close();

  void setFullscreen(bool on);
  bool isFullscreen() const { return m_fullscreen; }
  void toggleFullscreen();

  void setBorderless(bool on);
  bool isBorderless() const { return m_borderless; }
  void toggleBorderless();

  void setCursorVisible(bool visible);
  bool isCursorVisible() const { return m_cursorVisible; }
  void toggleCursorVisible();

  void setWindowGeometry(const QRect& g);

  void setForegroundColor(const QColor& c);
  void setBackgroundColor(const QColor& c);
  void setFont(const QFont& f);
  void setText(const QString& t);

  void setCommand(const QString& command, std::optional<double> intervalSec);

  void showColorDialog();
  void showTextColorDialog();
  void showTextDialog();
  void showContextMenu(const QPoint& globalPos);

private:
  void applyWindowMode();

  FlashlightModel* m_model = nullptr;
  FlashlightWidget* m_widget = nullptr;
  std::unique_ptr<TextGenerator> m_textGen;

  bool m_fullscreen = false;
  bool m_borderless = false;
  bool m_cursorVisible = true;
};

#endif
