import { useEffect, useMemo, useState } from 'react';
import Home from './firemap/Home.jsx';
import Question from './firemap/Question.jsx';
import Result from './firemap/Result.jsx';
import Experiment from './firemap/Experiment.jsx';
import Advanced from './firemap/Advanced.jsx';
import Curation from './firemap/Curation.jsx';
import Share from './firemap/Share.jsx';
import FloatingFeedback from './firemap/FloatingFeedback.jsx';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from