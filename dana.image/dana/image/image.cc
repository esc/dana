//
// Copyright (C) 2006 Nicolas Rougier
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 2 of the
// License, or (at your option) any later version.
// $Id$

#include "saliency.h"

BOOST_PYTHON_MODULE(_image) {
    using namespace dana::image;
    Saliency::boost();
}