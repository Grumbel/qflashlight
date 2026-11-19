// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#include "flashlight_widget.hpp"
#include "application.hpp"
#include "flashlight_model.hpp"

#include <QMouseEvent>
#include <QKeyEvent>
#include <QContextMenuEvent>
#include <QPaintEvent>
#include <QPainter>
#include <QFontMetrics>
#include <QPalette>
#include <QIcon>

FlashlightWidget::FlashlightWidget(Application* app, QWidget* parent)
  : QWidget(parent)
  , m_app(app)
{
  setWindowTitle(tr("QFlashlight"));
  setAutoFillBackground(true);
  setWindowIcon(QIcon::fromTheme("qflashlight"));
}

void FlashlightWidget::mouseDoubleClickEvent(QMouseEvent* event)
{
  Q_UNUSED(event);
  m_app->toggleFullscreen();
}

void FlashlightWidget::mousePressEvent(QMouseEvent* event)
{
  if (event->button() == Qt::LeftButton) {
    m_pressPos = event->pos();
  }
}

void FlashlightWidget::mouseMoveEvent(QMouseEvent* event)
{
  if (event->buttons() & Qt::LeftButton) {
    const QPoint diff = event->pos() - m_pressPos;
    move(pos() + diff);
  }
}

void FlashlightWidget::contextMenuEvent(QContextMenuEvent* event)
{
  m_app->showContextMenu(event->globalPos());
}

void FlashlightWidget::keyPressEvent(QKeyEvent* event)
{
  switch (event->key()) {
    case Qt::Key_Escape:
    case Qt::Key_Q:
      m_app->close();
      break;
    case Qt::Key_F:
      m_app->toggleFullscreen();
      break;
    case Qt::Key_M:
      m_app->toggleCursorVisible();
      break;
    case Qt::Key_E:
      m_app->showTextDialog();
      break;
    case Qt::Key_C:
      m_app->showColorDialog();
      break;
    case Qt::Key_T:
      m_app->showTextColorDialog();
      break;
    case Qt::Key_B:
      m_app->toggleBorderless();
      break;
    default:
      QWidget::keyPressEvent(event);
      break;
  }
}

void FlashlightWidget::setFullscreen(bool fullscreen)
{
  if (fullscreen) {
    setWindowState(windowState() | Qt::WindowFullScreen);
  } else {
    setWindowState(windowState() & ~Qt::WindowFullScreen);
  }
}

void FlashlightWidget::setBorderless(bool borderless)
{
  if (borderless) {
    // Only change when not fullscreen to avoid flicker (matches Python)
    if (!(windowState() & Qt::WindowFullScreen)) {
      setWindowFlags(windowFlags() | Qt::FramelessWindowHint);
      show();
    }
  } else {
    setWindowFlags(windowFlags() & ~Qt::FramelessWindowHint);
    show();
  }
}

void FlashlightWidget::paintEvent(QPaintEvent* event)
{
  Q_UNUSED(event);
  FlashlightModel* model = m_app->model();

  QPalette pal = palette();
  pal.setColor(QPalette::Window, model->backgroundColor());
  setPalette(pal);

  const QString text = model->text();
  if (!text.isEmpty()) {
    QPainter painter(this);
    painter.setPen(model->foregroundColor());
    painter.setFont(model->font());

    const QFontMetrics fm(painter.font());
    // Multi-line aware size (equivalent to Python QFontMetrics.size with AlignCenter)
    const QRect br = fm.boundingRect(QRect(0, 0, 0, 0),
                                     Qt::AlignCenter | Qt::TextWordWrap,
                                     text);
    const int tw = qMax(1, br.width());
    const int th = qMax(1, br.height());

    // Scale to fit while preserving aspect (matches Python)
    const qreal srcAspect = tw / qreal(th);
    const qreal dstAspect = width() / qreal(qMax(1, height()));

    qreal sx, sy;
    if (srcAspect > dstAspect) {
      sx = width() / qreal(tw);
      sy = sx;
    } else {
      sy = height() / qreal(th);
      sx = sy;
    }

    painter.scale(sx, sy);
    painter.drawText(QRectF(0, 0, width() / sx, height() / sy),
                     Qt::AlignCenter | Qt::TextWordWrap, text);
  }
}
