#!/usr/bin/python

# mech.py is a Python module which allows you to define solvers for mechanical systems, as well as providing a broad range of built in mechanical systems.

settings = {
    "BASE_DIR":"/home/aresnick/nub/projects/mechpy/solvers/",
    }

from sympy import *

import re
import inspect
import logging
from sets import Set




# Can be DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(level=logging.INFO)


# Function: 
# Inputs:
# Outputs:
# Notes:
def importSolvers(solvers=[]):
    if not solvers == []:
        directory = slashDirectory(settings['BASE_DIR'])
        for solver in solvers:
            solverFilename = directory + solver + '.py' 
            execfile(solverFilename, globals())

# Function: 
# Inputs:
# Outputs:
# Notes:
def parseVariables(varDefs):
    assignParser = re.compile('([a-zA-Z]+)\s*=\s*(\S+)')
    varParser = re.compile('([a-zA-Z]+)\W*')
    varDict = {}
    for varDef in varDefs:
        match = assignParser.match(varDef)
        var, val = match.group(1), match.group(2)
        varDict[var] = val
        subVars = varParser.findall(val)
        if len(subVars) > 0:
            for subVar in subVars:
                varDict[subVar] = ''

    return varDict

# Function: defineVariables returns a dictionary mapping variables to their values
# Inputs:
# Outputs:
# Notes:
def defineVariables(givenVars, values):
    logging.debug('Defining', str(givenVars), 'as', str(values))
    varDict = {}
    pairings = zip(givenVars, values)
    for var, value in pairings:
        if not value == '':
            varDict[str(var)] = value
#        logging.debug('Mapped', str(var), 'to', str(value))

    return varDict

# Function:
# Inputs:
# Outputs:
# Notes:
def cantileveredBeam(givenVars, values):

    # intermediate variables
    I = (w*h**3)/12
 
    # fundamental equation
    eq = d-P*(L**3)/(3*F*I)


# Function: symbolify takes a list of variables and converts it into a list of Symbols
# Inputs: list of string names
# Outputs: list of Symbols set to their own names
# Notes:
def symbolify(variables):
    symbols = []
    for var in variables:
        symbols.append(Symbol(var))

    return symbols

# Function: createSolver takes a list of variables and an equation and returns a solver
# Inputs: list of variables, string representing the basic equation to be solved
# Outputs: a function which acts as a solver, taking a set of variables and a set of values and returning the solution
# Notes:  Need to implement string interpolation or a parser to remove eval: significant capacity for abuse
def createSolver(basicEq, definedVars=''):
    varExtractor = re.compile('([a-zA-z]+)\W*')
    allVars = varExtractor.findall(basicEq)
    
    if not definedVars == '':
        allVars.extend(parseVariables(definedVars).keys())

    varVals = parseVariables(definedVars).values()
    varDefs = filter(lambda var: var != '', varVals)
            
    def solver(givenVars, allVars=allVars, basicEq=basicEq):
        givenVars = parseVariables(givenVars)
        givenVals = givenVars.values()
        givenVars = givenVars.keys()

        undefinedVars = list(Set(allVars).difference(Set(givenVars)))
        undefinedVars = symbolify(undefinedVars)

        allVars = symbolify(allVars)
        for var in allVars:
            globals()[str(var)] = var

        varDefs = parseVariables(definedVars)
        if varDefs != '':
            for var in varDefs.keys():
                globals()[str(var)] = varDefs[var]
            
        varValues = defineVariables(givenVars, givenVals)
        basicEq = eval(str(eval("basicEq")))
        for var in givenVars:
            basicEq = basicEq.subs(var, varValues[var])
        
        solns = solve(basicEq, undefinedVars)
        
        for var, sol in zip(undefinedVars, solns):
            print var, 'solved as', sol
            
        return solns

    return solver


def slashDirectory(directory):
    haveSlash = re.compile('.*/$')
    if not haveSlash.match(directory):
        directory += '/'
        
    return directory


def writeSolver(solver, name, directory = settings["BASE_DIR"]):
    directory = slashDirectory(directory)
    
    solverFilename = directory + name + '.py'

    fileOut = open(solverFilename, 'w')
    fileOut.write(inspect.getsource(solver))
    fileOut.close()

    return solverFilename
