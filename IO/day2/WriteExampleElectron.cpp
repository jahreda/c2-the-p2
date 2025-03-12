/*
 *  Copyright (C) 2002-2024 CERN for the benefit of the ATLAS collaboration
 */

#include "WriteExampleElectron.h"

// the user data-class defintions
#include "AthenaPoolExampleData/ExampleElectron.h"
#include "AthenaPoolExampleData/ExampleElectronAuxContainer.h"
#include "AthenaPoolExampleData/ExampleElectronContainer.h"
#include "AthenaPoolExampleData/ExampleHitContainer.h"
#include "AthenaPoolExampleData/ExampleTrackContainer.h"
#include "GaudiKernel/EventContext.h"
#include "StoreGate/WriteDecorHandle.h"
#include "StoreGate/WriteHandle.h"

using namespace AthPoolEx;

//___________________________________________________________________________
WriteExampleElectron::WriteExampleElectron(const std::string& name,
                                           ISvcLocator* pSvcLocator)
    : AthReentrantAlgorithm(name, pSvcLocator) {}

//___________________________________________________________________________
StatusCode WriteExampleElectron::initialize() {
  ATH_MSG_INFO(name() << ": in initialize()");

  ATH_CHECK(m_exampleElectronContainerKey.initialize());
  ATH_CHECK(m_exampleTrackKey.initialize());
  ATH_CHECK(m_exampleHitKey.initialize());
  ATH_CHECK(m_decor1Key.initialize());
  ATH_CHECK(m_decor2Key.initialize());
  ATH_CHECK(m_decor_floatKey.initialize());
  ATH_CHECK(m_decor_longdoubleKey.initialize());

  return StatusCode::SUCCESS;
}

//___________________________________________________________________________
StatusCode WriteExampleElectron::execute(const EventContext& ctx) const {
  ATH_MSG_DEBUG("WriteExampleElectron in execute()");
  std::size_t idx_trk = 0;
  std::size_t MAX = 100;
  float idx_decor = 0.0f;
  float trackPt = 0.0f;

  auto elecCont = std::make_unique<xAOD::ExampleElectronContainer>();
  auto elecStore = std::make_unique<xAOD::ExampleElectronAuxContainer>();
  elecCont->setStore(elecStore.get());

  /*
   * Convert ExampleTrack to xAOD::ExampleElectron
   */

  SG::ReadHandle<ExampleTrackContainer> trackCont(m_exampleTrackKey, ctx);

  elecCont->push_back(std::make_unique<xAOD::ExampleElectron>());

  for (const ExampleTrack* track : *trackCont) {
    trackPt = track->getPT(); 
    ATH_MSG_INFO(name() << ": track # " << idx_trk << " pT = " << trackPt 
                        << ".");

    // Push 10 electrons
    for(size_t idx = 0; idx < MAX; ++idx) {
    	// proceed to take this tracks pT
    	elecCont->back()->setPt(trackPt);
  	ATH_MSG_INFO(name() << ": idx: "<< idx << " Pt= " << elecCont->back()->pt() 
      			    << ";");

    }


    // Print out the pT that's being saved
    ATH_MSG_INFO(name() << ": track # " << idx_trk
                        << "is an electron with pT = " << elecCont->back()->pt()
                        << ";");

    idx_trk++;
  }
  
  SG::WriteHandle<xAOD::ExampleElectronContainer> objs(
      m_exampleElectronContainerKey, ctx);
	
  ATH_CHECK(objs.record(std::move(elecCont), std::move(elecStore)));
  

  /*
   * Writing Decorations
   */

  // WriteDecorHandle for the decoration 'TestContainer.decor1'
  SG::WriteDecorHandle<xAOD::ExampleElectronContainer, float> hdl1(m_decor1Key,
                                                                   ctx);

  // And for the second decoration 'TestContainer.decor2'
  SG::WriteDecorHandle<xAOD::ExampleElectronContainer, float> hdl2(m_decor2Key,
								 ctx);

  // Create WriteDecorHandle for each decoration
  SG::WriteDecorHandle<xAOD::ExampleElectronContainer, float> hdlF(m_decor_floatKey,
                                                                   ctx);

  SG::WriteDecorHandle<xAOD::ExampleElectronContainer, long double> hdl_LD(m_decor_longdoubleKey,
                                                                   ctx);
  if (objs.isValid()) {
    // Loop through objs to inspect
    for (const xAOD::ExampleElectron* obj: *objs) {
    	ATH_MSG_INFO(name() << ": Inspecting object with pt = " << obj->pt()
			    << ", charge = " << obj->charge());
    }

    // Access example electrons
    for (const xAOD::ExampleElectron* obj : *objs) {
      hdl1(*obj) = 115.9 + 12.34 * idx_decor;  // decor1
      hdl2(*obj) = 114.9 + idx_decor;          // decor2
     
      // for each object, assign the value you want to using the handle
      hdlF(*obj) = 115.+ (idx_decor*idx_decor); 
      hdl_LD(*obj) = (0.12346 * idx_decor) + 115.11511; 
	      
      // Verify writing out two decorations
      ATH_MSG_INFO(name() << ": DecorationWriter: decor1 = " << hdl1(*obj)
                          << ", decor2 = " << hdl2(*obj) << ";"
                          << ", decor_float= " << hdlF(*obj) << ";  "
                          << ", decor_longDouble = " << hdl_LD(*obj) << "!");
      idx_decor++;
    }
  } else {
    ATH_MSG_ERROR(name() << ": objs is not valid");
  }

  
  

  ATH_MSG_INFO(name() << ": registered all data");
  return StatusCode::SUCCESS;
}

//___________________________________________________________________________
StatusCode WriteExampleElectron::finalize() {
  ATH_MSG_INFO(name() << ": in finalize()");
  return StatusCode::SUCCESS;
}
