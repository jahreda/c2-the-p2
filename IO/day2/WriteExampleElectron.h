/*
  Copyright (C) 2002-2024 CERN for the benefit of the ATLAS collaboration
*/

#ifndef ATHENAPOOLEXAMPLEALGORITHMS_WRITEEXAMPLEELECTRON_H
#define ATHENAPOOLEXAMPLEALGORITHMS_WRITEEXAMPLEELECTRON_H

/** @file AthenaPoolExampleAlgorithms/src/WriteExampleElectron.h
 *  @brief This file contains the class definition for the WriteExampleElectron
 *class.
 **/

#include "AthenaBaseComps/AthReentrantAlgorithm.h"
#include "AthenaPoolExampleData/ExampleElectronContainer.h"
#include "AthenaPoolExampleData/ExampleHitContainer.h"
#include "AthenaPoolExampleData/ExampleTrackContainer.h"
#include "StoreGate/WriteDecorHandleKey.h"
#include "StoreGate/WriteHandleKey.h"

namespace AthPoolEx {

/** @class AthPoolEx::WriteExampleElectron
 *  @brief This class provides an example for writing event data objects to
 *Pool.
 **/
class WriteExampleElectron : public AthReentrantAlgorithm {
 public:  // Constructor and Destructor
  /// Standard Service Constructor
  WriteExampleElectron(const std::string& name, ISvcLocator* pSvcLocator);
  /// Destructor
  virtual ~WriteExampleElectron() = default;

 public:
  /// Gaudi Service Interface method implementations:
  virtual StatusCode initialize() override final;
  virtual StatusCode execute(const EventContext& ctx) const override final;
  virtual StatusCode finalize() override final;

  // Read in ExampleTracks and ExampleHits
  SG::ReadHandleKey<ExampleTrackContainer> m_exampleTrackKey{
      this, "ExampleTrackKey", "MyTracks"};
  SG::ReadHandleKey<ExampleHitContainer> m_exampleHitKey{this, "ExampleHitKey",
                                                         "MyHits"};

  // We will want to write some of those tracks as an ExampleElectron and place
  // them into a container
  SG::WriteHandleKey<xAOD::ExampleElectronContainer>
      m_exampleElectronContainerKey{this, "ExampleElectronContainerName",
                                    "TestContainer"};

  // Testing writing decorations, need keys
  SG::WriteDecorHandleKey<xAOD::ExampleElectronContainer> m_decor1Key{
      this, "ExampleElectronContainerDecorKey1", "TestContainer.decor1",
      "decorator1 key"};
  SG::WriteDecorHandleKey<xAOD::ExampleElectronContainer> m_decor2Key{
      this, "ExampleElectronContainerDecorKey2", "TestContainer.decor2",
      "decorator2 key"};
  
  SG::WriteDecorHandleKey<xAOD::ExampleElectronContainer> m_decor_floatKey{
      this, "ExampleElectronContainerDecorKeyFloat", "TestContainer.decor_float",
      "decorator for float key"};
  
  SG::WriteDecorHandleKey<xAOD::ExampleElectronContainer> m_decor_longdoubleKey{
      this, "ExampleElectronContainerDecorKeyLongDouble", "TestContainer.decor_longdouble",
      "decorator for long double key"};
};

}  // namespace AthPoolEx

#endif
