'''
I completed this project as part of my MITx 6.00.2x Introduction to Computational Thinking and Data Science
curriculum. It runs a simulation of the spread of a virus and compares the results of the spread over time with a drug
to the results without a drug taking into account the virus becoming resistant and creates a visual representation using pylab.

The values can be altered to simulate different hypothetical scenarios.
Alter values on lines 238 (without drug) and 551 (with drug)


simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials)

simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials)

Runs simulations and plots graphs for problem 5.

For each of numTrials trials, instantiates a patient, runs a simulation for
150 timesteps, adds guttagonol, and runs the simulation for an additional
150 timesteps.  At the end plots the average virus population size
(for both the total virus population and the guttagonol-resistant virus
population) as a function of time.

numViruses: number of ResistantVirus to create for patient (an integer)
maxPop: maximum virus population for patient (an integer)
maxBirthProb: Maximum reproduction probability (a float between 0-1)        
clearProb: maximum clearance probability (a float between 0-1)
resistances: a dictionary of drugs that each ResistantVirus is resistant to
             (e.g., {'guttagonol': False})
mutProb: mutation probability for each ResistantVirus particle
         (a float between 0-1). 
numTrials: number of simulation runs to execute (an integer)
    
''' 

import random
import pylab



class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        if random.random() <= self.clearProb:
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        if random.random() <= self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)      


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        dead = []
        for i in range(len(self.viruses)):
            if self.viruses[i].doesClear():
                dead.append(i)
        dead.reverse()
        for i in dead:
            del self.viruses[i]
        new = []
        popDens = len(self.viruses) / float(self.maxPop)
        for i in self.viruses:
            try:
                new.append(i.reproduce(popDens))
            except NoChildException:
                a = 0
        self.viruses = self.viruses + new
        return len(self.viruses)



def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    a_list = []    # Averages
    d_list = []    # Data nested
    for trial in range(numTrials):
        viruses = []    # Initial Viruses
        t_list = []    # Trial sublist
        for v in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        pat = Patient(viruses, maxPop)
        for i in range(300):
            t_list.append(pat.update())
        d_list.append(t_list)           # Createted nest data list
    for n in range(300):
        a_list.append(0)
    for t in d_list:                    # Get averages
        for p in range(len(t)):
            a_list[p] = a_list[p] + t[p]
    for a in range(len(a_list)):
        a_list[a] = a_list[a] / float(numTrials)
    pylab.plot(a_list, label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()
# Alter values below for a customized simulation
simulationWithoutDrug(100, 1000, .1, .05, 10)
            



class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        if drug in self.resistances:
            if self.resistances[drug] == True:
                return True
        return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        flag = True
        new_resistance = {}
        for drug in activeDrugs:
            if ResistantVirus.isResistantTo(self, drug) == False:
                flag = False
        if flag == True and random.random() <= self.maxBirthProb * (1 - popDensity):
            for d in self.resistances.keys():
                if self.resistances[d] == True:
                    if random.random() <= self.mutProb:
                        new_resistance[d] = False
                    else:
                        new_resistance[d] = True
                elif self.resistances[d] == False:
                    if random.random() <= self.mutProb:
                        new_resistance[d] = True
                    else:
                        new_resistance[d] = False
            return ResistantVirus(self.maxBirthProb, self.clearProb, new_resistance, self.mutProb)
        else:
            raise NoChildException()


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.ba = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.ba:
            self.ba.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.ba


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        rv = 0
        for v in self.viruses:
            flag = True
            for dr in drugResist:
                if v.isResistantTo(dr) == False:
                    flag = False
            if flag == True:
                rv += 1
        return rv


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        dead = []
        for i in range(len(self.viruses)):
            if random.random() <= self.viruses[i].getClearProb():
                dead.append(i)
        dead.reverse()
        for d in dead:
            del self.viruses[d]
        popD = len(self.viruses) / float(self.maxPop)
        nv = []
        for v in self.viruses:
            try:
                a = v.reproduce(popD, self.ba)
            except NoChildException:
                a = 0
            if type(a) != None and type(a) != int:
                nv.append(a)
        self.viruses = self.viruses + nv
        return len(self.viruses)



def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    L = []
    lg = []
    for trial in range(numTrials):
        viruses = []
        for vir in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        tom = TreatedPatient(viruses, maxPop)
        sub = []
        sg = []
        for i in range(150):
            gc = 0
            sub.append(tom.update())
            for g in tom.getViruses():
                if g.isResistantTo("guttagonol"):
                    gc += 1
            sg.append(gc)
        tom.addPrescription("guttagonol")
        for i in range(150):
            gc = 0
            sub.append(tom.update())
            for g in tom.getViruses():
                if g.isResistantTo("guttagonol"):
                    gc += 1
            sg.append(gc)
        L.append(sub)
        lg.append(sg)
    av = []
    for i in range(300):
        av.append(0)
    for s in L:
        for i in range(len(s)):
            av[i] += s[i]
    for i in range(len(av)):
        av[i] = av[i] / float(numTrials)
    ag = []
    for i in range(300):
        ag.append(0)
    for j in lg:
        for i in range(len(j)):
            ag[i] += j[i]
    for i in range(len(ag)):
        ag[i] = ag[i] / float(numTrials)
    pylab.plot(av, label = "total virus population")
    pylab.plot(ag, label = "guttagonol-resistant virus")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()
# Alter values below for a customized simulation
simulationWithDrug(100, 1000, .1, .05, {'guttagonol': False}, 0.005, 10)            
        
