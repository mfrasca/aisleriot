/*
 * Copyright © 2007 Christian Persch
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef AISLERIOT_WINDOW_H
#define AISLERIOT_WINDOW_H

#include <gtk/gtk.h>

#include "game.h"

G_BEGIN_DECLS

#define AISLERIOT_TYPE_WINDOW         (aisleriot_window_get_type ())
#define AISLERIOT_WINDOW(o)           (G_TYPE_CHECK_INSTANCE_CAST ((o), AISLERIOT_TYPE_WINDOW, AisleriotWindow))
#define AISLERIOT_WINDOW_CLASS(k)     (G_TYPE_CHECK_CLASS_CAST((k), AISLERIOT_TYPE_WINDOW, AisleriotWindowClass))
#define AISLERIOT_IS_WINDOW(o)        (G_TYPE_CHECK_INSTANCE_TYPE ((o), AISLERIOT_TYPE_WINDOW))
#define AISLERIOT_IS_WINDOW_CLASS(k)  (G_TYPE_CHECK_CLASS_TYPE ((k), AISLERIOT_TYPE_WINDOW))
#define AISLERIOT_WINDOW_GET_CLASS(o) (G_TYPE_INSTANCE_GET_CLASS ((o), AISLERIOT_TYPE_WINDOW, AisleriotWindowClass))

typedef struct _AisleriotWindow	        AisleriotWindow;
typedef struct _AisleriotWindowPrivate  AisleriotWindowPrivate;

struct _AisleriotWindow {
  GtkWindow parent_instance;

  /*< private >*/
  AisleriotWindowPrivate *priv;
};

typedef GtkWindowClass AisleriotWindowClass;

GType aisleriot_window_get_type (void);

GtkWidget *aisleriot_window_new (gboolean freecell_mode);

void aisleriot_window_set_game_module (AisleriotWindow * window,
                                       const char *game_module,
                                       GRand *rand);

const char *aisleriot_window_get_game_module (AisleriotWindow *window);

G_END_DECLS

#endif /* !AISLERIOT_WINDOW_H */
