import os
import discord
from discord.ext import commands
import math
import matplotlib.pyplot as plt
import numpy as np
from sympy.solvers import solve
from sympy import Symbol, divisors
from sympy.ntheory import primefactors, isprime

from asteval import Interpreter
aeval = Interpreter()

import wolframalpha
appid = os.environ['APP_ID']
app = wolframalpha.Client(appid)

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.command(name="evaluate", aliases=["eval"])
async def evaluate(ctx, expr):
    try:
        x = aeval(expr)
        await ctx.send(f"{expr} = {x}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name='graph')
async def graph(ctx, expr, grid=True):
    try:
        x = np.linspace(-10, 10, 1000)
        y = eval(expr)
        plt.plot(x, y)
        if grid is True:
            plt.grid()
        plt.savefig('graph.png')
        await ctx.send(f"The graph of {expr} is:")
        await ctx.send(file=discord.File('graph.png'))
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="query", aliases=["ask"])
async def query(ctx, question):
    res = app.query(question)
    if res['@success'] == 'false':
        await ctx.send('I was unable to find an answer to your question.')
    else:
        answer = next(res.results).text
        await ctx.send(f'The answer to your question is {answer}')

@client.command(name="solve")
async def solve_(ctx, equation, symbol):
    try:
        x = Symbol(symbol)
        solution = solve(equation, x)
        await ctx.send(f"The solutions to {equation} are {solution}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="isprime")
async def isprime_(ctx, n):
    try:
        if isprime(int(n)) == True:
            await ctx.send(f"{n} is prime.")
        else:
            await ctx.send(f"{n} is not prime.")
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="primefactor")
async def primefactor(ctx, n):
    try:
        x = primefactors(n)
        await ctx.send(f"The prime factors of {n} are {x})
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="divisors")
async def primefactor(ctx, n):
    try:
        x = divisors(n)
        await ctx.send(f"The divisors of {n} are {x})
    except:
        await ctx.send("There's been an error! Modify your input.")
                       
@client.command(name="goat")
async def goat(ctx):
    await ctx.send("Euler is the Greatest of All Time in mathematics.")

token = os.environ['DISCORD_BOT_SECRET']
client.run(token)
