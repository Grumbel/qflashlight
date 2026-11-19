// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#ifndef QFLASHLIGHT_FLASHLIGHT_WIDGET_HPP
#define QFLASHLIGHT_FLASHLIGHT_WIDGET_HPP

#include <QWidget>
#include <QPoint>

class Application;
class QMouseEvent;
class QKeyEvent;
class QContextMenuEvent;
class QPaintEvent;

class FlashlightWidget : public QWidget
{
  Q_OBJECT

public:
  explicit FlashlightWidget(Application* app, QWidget* parent = nullptr);

  void setFullscreen(bool fullscreen);
  void setBorderless(bool borderless);

protected:
  void mouseDoubleClickEvent(QMouseEvent* event) override;
  void mousePressEvent(QMouseEvent* event) override;
  void mouseMoveEvent(QMouseEvent* event) override;
  void contextMenuEvent(QContextMenuEvent* event) override;
  void keyPressEvent(QKeyEvent* event) override;
  void paintEvent(QPaintEvent* event) override;

private:
  Application* m_app;
  QPoint m_pressPos;
};

#endif
