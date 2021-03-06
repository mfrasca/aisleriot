/*
 * Copyright © 1998, 2001, 2003, 2006 Jonathan Blandford <jrb@alum.mit.edu>
 * Copyright © 2007 Christian Persch
 * Copyright © 2007 Andreas Røsdal <andreasr@gnome.org> 
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

#include <config.h>

#include <string.h>

#include <libguile.h>

#include <glib.h>
#include <glib/gi18n.h>

#include <gtk/gtk.h>

#ifdef HAVE_CLUTTER
#include <cogl/cogl.h>
#include <clutter/clutter.h>
#include <clutter-gtk/clutter-gtk.h>
#endif

#include "ar-debug.h"
#include "ar-stock.h"
#include "ar-runtime.h"
#include "ar-sound.h"

#include "ar-string-utils.h"
#include "conf.h"
#include "window.h"
#include "game.h"
#include "util.h"

#if 0
/* String reserve */
N_("Solitaire")
N_("GNOME Solitaire")
N_("About Solitaire")
#endif /* 0 */

typedef struct {
  AisleriotWindow *window;
  char *variation;
  gint seed; /* unused */
  gboolean freecell;
} AppData;

static void
add_main_options (GOptionContext *option_context,
                  AppData *data)
{
  const GOptionEntry aisleriot_options[] = {
    { "variation", 'v', 0, G_OPTION_ARG_STRING, &data->variation,
      N_("Select the game type to play"), N_("NAME") },
    { "freecell", 0, G_OPTION_FLAG_HIDDEN, G_OPTION_ARG_NONE, &data->freecell,
      NULL, NULL },

    /* Ignored option, for backward compat with saved session */
    { "seed", 's', G_OPTION_FLAG_HIDDEN, G_OPTION_ARG_STRING, &data->seed,
      NULL, NULL },

    { NULL }
  };

  g_option_context_add_main_entries (option_context,
				     aisleriot_options, GETTEXT_PACKAGE);
}

static void
main_prog (void *closure, int argc, char *argv[])
{
  AppData data;
  GOptionContext *option_context;
  GError *error = NULL;
  gboolean retval;

  memset (&data, 0, sizeof (AppData));

  option_context = g_option_context_new (NULL);
  g_option_context_set_translation_domain (option_context, GETTEXT_PACKAGE);

  add_main_options (option_context, &data);

  ar_sound_enable (FALSE);

  g_option_context_add_group (option_context, gtk_get_option_group (TRUE));

#ifdef HAVE_CLUTTER
  g_option_context_add_group (option_context, cogl_get_option_group ());
  g_option_context_add_group (option_context, clutter_get_option_group_without_init ());
  g_option_context_add_group (option_context, gtk_clutter_get_option_group ());
#endif /* HAVE_CLUTTER */

  retval = g_option_context_parse (option_context, &argc, &argv, &error);
  g_option_context_free (option_context);

  if (!retval) {
    g_printerr ("%s\n", error->message);
    g_error_free (error);
    goto cleanup;
  }

  g_set_application_name (data.freecell ? _("FreeCell Solitaire") : _("AisleRiot"));

  aisleriot_conf_init ();

  /* If we are asked for a specific game, check that it is valid. */
  if (!data.freecell &&
      data.variation != NULL) {
    char *game_module = NULL;

    if (data.variation[0] != '\0') {
      game_module = ar_filename_to_game_module (data.variation);
    }

    g_free (data.variation);
    data.variation = game_module;
  }

  if (!data.freecell && !data.variation) {
    char *pref;

    pref = ar_conf_get_string_with_default (NULL, aisleriot_conf_get_key (CONF_VARIATION), DEFAULT_VARIATION);
    data.variation = ar_filename_to_game_module (pref);
    g_free (pref);
  }

  g_assert (data.variation != NULL || data.freecell);

  ar_stock_init ();

  gtk_window_set_default_icon_name (data.freecell ? "gnome-freecell" : "gnome-aisleriot");

  data.window = AISLERIOT_WINDOW (aisleriot_window_new (data.freecell));
  g_signal_connect (data.window, "destroy",
		    G_CALLBACK (gtk_main_quit), NULL);

  if (data.freecell) {
    aisleriot_window_set_game_module (data.window, FREECELL_VARIATION, NULL);
  } else {
    aisleriot_window_set_game_module (data.window, data.variation, NULL);
  }

  gtk_window_present (GTK_WINDOW (data.window));

  gtk_main ();

  aisleriot_conf_shutdown ();

cleanup:
  g_free (data.variation);

  g_settings_sync ();

  ar_runtime_shutdown ();
}

int
main (int argc, char *argv[])
{
  if (!ar_runtime_init ("aisleriot"))
    return 1;

  g_setenv ("GUILE_WARN_DEPRECATED", "detailed", TRUE);
  g_setenv ("GUILE_AUTO_COMPILE", "0", TRUE);

  g_setenv ("UBUNTU_MENUPROXY", "0", TRUE);

  scm_boot_guile (argc, argv, main_prog, NULL); /* no return */

  return 0;
}
