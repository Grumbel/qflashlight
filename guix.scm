;; qflashlight - Simple Qt-based fullscreen flashlight
;; Copyright (C) 2019 Ingo Ruhnke <grumbel@gmail.com>
;;
;; This program is free software: you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.
;;
;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

(use-modules (guix packages)
             (guix gexp)
             (guix git-download)
             (guix build-system python)
             (guix licenses)
             (gnu packages qt))

(define %source-dir (dirname (current-filename)))

(define-public qflashlight
  (package
    (name "qflashlight")
    (version "0.1.0")
    (source
     (local-file %source-dir
                 #:recursive? #t
                 #:select? (git-predicate %source-dir)))
    (build-system python-build-system)
    (inputs
     `(("python-pyqt" ,python-pyqt)))
    (home-page "https://gitlab.com/grumbel/qflashlight")
    (synopsis "Fill the screen with a solid color or text banner")
    (description "QFlashlight is a simple Qt application that will
fill the whole screen with a solid color.  The color can be selected
via command line with `--color` optional or interactively via the
color picker (press 'C').  Fullscreen can be entered and left with a
double click. The mouse cursor can be hidden by pressing 'M'.")
    (license gpl3+)))

qflashlight

;; EOF ;;
