/*
  Copyright © 2004 Callum McKenzie
  Copyright © 2007, 2008 Christian Persch

  This programme is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This programme is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this programme.  If not, see <http://www.gnu.org/licenses/>. */

/* Authors:   Callum McKenzie <callum@physics.otago.ac.nz> */

#include <config.h>

#include <string.h>
#include <glib.h>
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <gtk/gtk.h>

#include "games-find-file.h"
#include "games-files.h"
#include "games-preimage.h"
#include "games-preimage-private.h"
#include "games-runtime.h"

#include "games-card-theme.h"
#include "games-card-theme-private.h"

struct _GamesCardThemeKDEClass {
  GamesCardThemePreimageClass parent_class;
};

struct _GamesCardThemeKDE {
  GamesCardThemePreimage parent_instance;
};

#include <librsvg/librsvg-features.h>
#if defined(HAVE_RSVG) && defined(LIBRSVG_CHECK_VERSION) && LIBRSVG_CHECK_VERSION(2, 22, 4)
#define HAVE_RSVG_BBOX
#endif

#define N_ROWS ((double) 5.0)
#define N_COLS ((double) 13.0)

#define DELTA (0.0f)

/* #defining this prints out the time it takes to render the theme */
/* #define INSTRUMENT_LOADING */

#ifdef INSTRUMENT_LOADING
static long totaltime = 0;
#endif

/* Class implementation */

G_DEFINE_TYPE (GamesCardThemeKDE, games_card_theme_kde, GAMES_TYPE_CARD_THEME_PREIMAGE);

static gboolean
games_card_theme_kde_load (GamesCardTheme *card_theme,
                           GError **error)
{
  GamesCardThemePreimage *preimage_card_theme = (GamesCardThemePreimage *) card_theme;
  gboolean retval = FALSE;

#ifdef INSTRUMENT_LOADING
  clock_t t1, t2;

  t1 = clock ();
#endif

  if (!GAMES_CARD_THEME_CLASS (games_card_theme_kde_parent_class)->load (card_theme, error))
    goto out;

#ifndef HAVE_RSVG_BBOX
  goto out;
#endif

  if (!games_preimage_is_scalable (preimage_card_theme->cards_preimage))
    goto out;

  retval = TRUE;

out:

#ifdef INSTRUMENT_LOADING
  t2 = clock ();
  totaltime += (t2 - t1);
  g_print ("took %.3fs to create preimage (cumulative %.3fs)\n",
           (t2 - t1) * 1.0 / CLOCKS_PER_SEC,
           totaltime * 1.0 / CLOCKS_PER_SEC);
#endif

  return retval;
}

static GdkPixbuf *
games_card_theme_kde_get_card_pixbuf (GamesCardTheme *card_theme,
                                      int card_id)
{
#ifndef HAVE_RSVG_BBOX
  GamesCardThemePreimage *preimage_card_theme = (GamesCardThemePreimage *) card_theme;
  GamesPreimage *preimage = preimage_card_theme->cards_preimage;
  GdkPixbuf *subpixbuf;
  int suit, rank;
  double card_width, card_height;
  double width, height;
  double zoomx, zoomy;
  char node[64];
  RsvgDimensionData dimension;
  RsvgPositionData position;

  suit = card_id / 13;
  rank = card_id % 13;

  if (G_UNLIKELY (card_id == GAMES_CARD_SLOT)) {
    subpixbuf = games_preimage_render (preimage_card_theme->slot_preimage,
                                       preimage_card_theme->card_size.width,
                                       preimage_card_theme->card_size.height);

    return subpixbuf;
  }

  games_card_get_node_by_suit_and_rank_snprintf (node, sizeof (node), suit, rank);

  if (!rsvg_handle_get_dimension_sub (preimage->rsvg_handle, &dimension, node) ||
      !rsvg_handle_get_position_sub (preimage->rsvg_handle, &position, node)) {
    g_print ("Failed to get dim or pos for '%s'\n", node);
    return NULL;
  }

  card_width = ((double) games_preimage_get_width (preimage)) / N_COLS;
  card_height = ((double) games_preimage_get_height (preimage)) / N_ROWS;

  width = preimage_card_theme->card_size.width - 2 * DELTA;
  height = preimage_card_theme->card_size.height - 2 * DELTA;

  zoomx = width / dimension.width;
  zoomy = height / dimension.height;

  subpixbuf = games_preimage_render_sub (preimage,
                                         node,
                                         preimage_card_theme->card_size.width,
                                         preimage_card_theme->card_size.height,
                                         -position.x, -position.y,
                                         zoomx, zoomy);

  return subpixbuf;
#else
  return NULL;
#endif
}

static void
games_card_theme_kde_init (GamesCardThemeKDE * cardtheme)
{
}

static GamesCardThemeInfo *
games_card_theme_kde_class_get_theme_info (GamesCardThemeClass *klass,
                                           const char *path,
                                           const char *filename)
{
  if (!g_str_has_suffix (filename, ".svgz")) // FIXMEchpe 
    return NULL;

  return _games_card_theme_info_new (G_OBJECT_CLASS_TYPE (klass),
                                     path,
                                     filename, /* FIXME */
                                     filename, /* FIXME */
                                     NULL, NULL);
}

static void
games_card_theme_kde_class_get_theme_infos (GamesCardThemeClass *klass,
                                            GList **list)
{
  _games_card_theme_class_append_theme_info_foreach_env
    (klass, "GAMES_CARD_THEME_PATH_KDE", list);

  _games_card_theme_class_append_theme_info_foreach
    (klass, games_runtime_get_directory (GAMES_RUNTIME_SCALABLE_CARDS_DIRECTORY), list);
}

static void
games_card_theme_kde_class_init (GamesCardThemeKDEClass * klass)
{
  GamesCardThemeClass *theme_class = GAMES_CARD_THEME_CLASS (klass);

  theme_class->get_theme_info = games_card_theme_kde_class_get_theme_info;
  theme_class->get_theme_infos = games_card_theme_kde_class_get_theme_infos;

  theme_class->load = games_card_theme_kde_load;
  theme_class->get_card_pixbuf = games_card_theme_kde_get_card_pixbuf;
}

/* private API */

/**
 * games_card_theme_kde_new:
 *
 * Returns: a new #GamesCardThemeKDE
 */
GamesCardTheme*
games_card_theme_kde_new (void)
{
  return g_object_new (GAMES_TYPE_CARD_THEME_KDE, NULL);
}