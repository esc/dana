//
// Copyright (C) 2006,2007 Nicolas Rougier
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 2 of the
// License, or (at your option) any later version.
//
// $Id: model.h 241 2007-07-19 08:52:13Z rougier $

#ifndef __DANA_CORE_MODEL_H__
#define __DANA_CORE_MODEL_H__

#include <boost/thread/barrier.hpp>
#include <vector>
#include "object.h"
#include "network.h"
#include "environment.h"

namespace dana { namespace core {

    typedef boost::shared_ptr<class Model> ModelPtr;

    // ____________________________________________________________class Object
    class Model : public Object {

        // ___________________________________________________________attributes
    public:
        std::vector<NetworkPtr>     networks;
        std::vector<EnvironmentPtr> environments;
        SpecPtr                     spec;
        bool                        running;
        boost::barrier *            barrier;
        unsigned long               age;
        unsigned long               time, start_time, stop_time;
        static Model *              current_model;
        
    public:
        // _________________________________________________________________life
        Model (void);
        virtual ~Model (void);

        // _________________________________________________________________main
        virtual void        append (NetworkPtr net);
        virtual void        append (EnvironmentPtr env);
        virtual void        clear (void);
        virtual bool        start (unsigned long n=0);
        virtual void        stop (void);
        static void         entry_point (void);

        // ______________________________________________________________get/set
        virtual SpecPtr       get_spec (void);
        virtual void          set_spec (SpecPtr spec);  
        
        // _______________________________________________________________export
        static void         python_export (void);
    };
}}

#endif
