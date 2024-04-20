import './App.scss'
import { Routes, Route } from 'react-router-dom'
import Login from './components/login'
import Layout from './components/layout'
import Home from './components/home'
import Signup from './components/signup'
import Settings from './components/settings'
import OnBoardMF from './components/onboarding/onboardmf'
import OnBoardHeight from './components/onboarding/onboardheight'
import OnboardingLayout from './components/onboarding/onboardinglayout'
import OnBoardWeight from './components/onboarding/onboardweight'
import OnBoardFitGoal from './components/onboarding/onboardfitgoal'
import OnBoardActiveLevel from './components/onboarding/onboardactivelevel'
import OnBoardTimeline from './components/onboarding/onboardtimeline'
import OnBoardAge from './components/onboarding/onboardAge'

function App() {
  

  return (
    <>
      <Routes>
        <Route path='login' element={<Login />} />
        <Route path='signup' element={<Signup />} />
        {/* <Route path='/onboarding/gender' element={<OnBoardMF />} />
        <Route path='/onboarding/height' element={<OnBoardHeight />} /> */}
        <Route path='onboarding' element={<OnboardingLayout />} >
          <Route path='gender' element={<OnBoardMF/>}/>
          <Route path='height' element={<OnBoardHeight/>}/>
          <Route path='weight' element={<OnBoardWeight />} />
          <Route path='fitgoals' element={<OnBoardFitGoal/>}/>
          <Route path='activelevel' element={<OnBoardActiveLevel/>}/>
          <Route path='timeline' element={<OnBoardTimeline/>}/>
          <Route path='age' element={<OnBoardAge/>}/>
        </Route>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path='settings' element={<Settings />} />
        </Route>
      </Routes>
    </>
  )
}

export default App