// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#include "application.hpp"
#include "flashlight_model.hpp"
#include "flashlight_widget.hpp"
#include "text_generator.hpp"

#include <QMenu>
#include <QColorDialog>
#include <QInputDialog>
#include <QPlainTextEdit>
#include <QDialog>
#include <QDialogButtonBox>
#include <QVBoxLayout>
#include <QApplication>

Application::Application(QObject* parent)
  : QObject(parent)
{
  m_model = new FlashlightModel(this);
  m_widget = new FlashlightWidget(this);
  connect(m_model, &FlashlightModel::changed, m_widget, QOverload<>::of(&QWidget::update));
}

Application::~Application() = default;

void Application::show()
{
  m_widget->show();
}

void Application::close()
{
  m_widget->close();
}

void Application::setFullscreen(bool on)
{
  m_fullscreen = on;
  applyWindowMode();
}

void Application::toggleFullscreen()
{
  m_fullscreen = !m_fullscreen;
  applyWindowMode();
}

void Application::setBorderless(bool on)
{
  m_borderless = on;
  applyWindowMode();
}

void Application::toggleBorderless()
{
  m_borderless = !m_borderless;
  applyWindowMode();
}

void Application::applyWindowMode()
{
  m_widget->setFullscreen(m_fullscreen);
  m_widget->setBorderless(m_borderless);
}

void Application::setWindowGeometry(const QRect& g)
{
  m_widget->setGeometry(g);
}

void Application::setCursorVisible(bool visible)
{
  m_cursorVisible = visible;
  if (m_cursorVisible) {
    m_widget->unsetCursor();
  } else {
    m_widget->setCursor(Qt::BlankCursor);
  }
}

void Application::toggleCursorVisible()
{
  setCursorVisible(!m_cursorVisible);
}

void Application::setForegroundColor(const QColor& c)
{
  m_model->setForegroundColor(c);
}

void Application::setBackgroundColor(const QColor& c)
{
  m_model->setBackgroundColor(c);
}

void Application::setFont(const QFont& f)
{
  m_model->setFont(f);
}

void Application::setText(const QString& t)
{
  m_textGen.reset();
  m_model->setText(t);
}

void Application::setCommand(const QString& command, std::optional<double> intervalSec)
{
  m_textGen = std::make_unique<TextGenerator>(
    command, intervalSec,
    [this](const QString& text) {
      m_model->setText(text);
      m_widget->update();
    },
    this);
  m_textGen->start();
}

void Application::showColorDialog()
{
  const QColor original = m_model->backgroundColor();
  QColorDialog* dlg = new QColorDialog(m_widget);
  dlg->setAttribute(Qt::WA_DeleteOnClose);
  dlg->setWindowModality(Qt::WindowModal);
  dlg->setCurrentColor(original);

  connect(dlg, &QColorDialog::currentColorChanged, m_model, &FlashlightModel::setBackgroundColor);
  connect(dlg, &QColorDialog::colorSelected, m_model, &FlashlightModel::setBackgroundColor);
  connect(dlg, &QColorDialog::rejected, this, [this, original]() {
    m_model->setBackgroundColor(original);
  });
  dlg->show();
}

void Application::showTextColorDialog()
{
  const QColor original = m_model->foregroundColor();
  QColorDialog* dlg = new QColorDialog(m_widget);
  dlg->setAttribute(Qt::WA_DeleteOnClose);
  dlg->setWindowModality(Qt::WindowModal);
  dlg->setCurrentColor(original);

  connect(dlg, &QColorDialog::currentColorChanged, m_model, &FlashlightModel::setForegroundColor);
  connect(dlg, &QColorDialog::colorSelected, m_model, &FlashlightModel::setForegroundColor);
  connect(dlg, &QColorDialog::rejected, this, [this, original]() {
    m_model->setForegroundColor(original);
  });
  dlg->show();
}

void Application::showTextDialog()
{
  // Simple modal-ish dialog matching the Python TextDialog behaviour
  QDialog* dlg = new QDialog(m_widget);
  dlg->setAttribute(Qt::WA_DeleteOnClose);
  dlg->setWindowTitle(tr("Change Text"));
  dlg->setWindowModality(Qt::WindowModal);
  dlg->resize(600, 200);

  auto* edit = new QPlainTextEdit(dlg);
  edit->setPlainText(m_model->text());
  auto* buttons = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, dlg);

  auto* layout = new QVBoxLayout(dlg);
  layout->addWidget(edit);
  layout->addWidget(buttons);

  const QString original = m_model->text();

  connect(edit, &QPlainTextEdit::textChanged, this, [this, edit]() {
    m_model->setText(edit->toPlainText());
  });
  connect(buttons, &QDialogButtonBox::accepted, dlg, &QDialog::accept);
  connect(buttons, &QDialogButtonBox::rejected, this, [this, original, dlg]() {
    m_model->setText(original);
    dlg->reject();
  });

  dlg->show();
}

void Application::showContextMenu(const QPoint& globalPos)
{
  QMenu menu;

  if (m_fullscreen) {
    menu.addAction(tr("Exit full screen"), this, [this]() { setFullscreen(false); });
  } else {
    menu.addAction(tr("Enter full screen"), this, [this]() { setFullscreen(true); });
  }

  if (m_cursorVisible) {
    menu.addAction(tr("Hide mouse cursor"), this, [this]() { setCursorVisible(false); });
  } else {
    menu.addAction(tr("Show mouse cursor"), this, [this]() { setCursorVisible(true); });
  }

  if (m_borderless) {
    menu.addAction(tr("Show window border"), this, [this]() { setBorderless(false); });
  } else {
    menu.addAction(tr("Hide window border"), this, [this]() { setBorderless(true); });
  }

  menu.addAction(tr("Change Color..."), this, &Application::showColorDialog);
  menu.addAction(tr("Change Text Color..."), this, &Application::showTextColorDialog);
  menu.addAction(tr("Change Text..."), this, &Application::showTextDialog);
  menu.addSeparator();
  menu.addAction(tr("Exit"), this, &Application::close);

  menu.exec(globalPos);
}
