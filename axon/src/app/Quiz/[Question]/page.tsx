'use client'
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import Confetti from 'react-confetti'
import { useWindowSize } from 'react-use';

import { motion } from 'framer-motion'
import { MaterialSymbolsArrowBackRounded, MaterialSymbolsFavoriteRounded } from "@/components/icons";
import { useRouter } from "next/navigation";
import useGameStore from "@/components/state";
import { useSession } from "next-auth/react";
import { Rubik } from "next/font/google";
import { config } from "@/config";
const rbk = Rubik({ subsets: ['latin'], weight: "900" })
export default function Page({ params }: { params: { Question: string } }) {
    const { width, height } = useWindowSize();
    const session = useSession()
    const router = useRouter()
    const [currentQuestion, setCurrentQuestion] = useState(0)
    const [isComplete, setCompleted] = useState(false)
    const [goNextState, setGoNext] = useState(false)
    const [selectedOption, setSelectedOption] = useState<string | null>(null)
    const [currentResult, setCurrentResult] = useState<1 | 0 | null>(null)
    const [gameOver, setGameOver] = useState<boolean>(false)
    const { playerLives, increasePlayerScore, decreasePlayerLives, playerScore } = useGameStore()
    const [mcq, setMCQ] = useState<any>(null)
    // const mcq = {
    //     questions: [
    //         {
    //             "question": "What is React?",
    //             "options": ["Library", "Framework", "Language", "Application"],
    //             "correct": "Library"
    //         },
    //         {
    //             "question": "What is Vue.js?",
    //             "options": ["Library", "Framework", "Language", "Database"],
    //             "correct": "Framework"
    //         },
    //         {
    //             "question": "What is Angular?",
    //             "options": ["Library", "Framework", "Language", "Server"],
    //             "correct": "Framework"
    //         },
    //         {
    //             "question": "What is JavaScript?",
    //             "options": ["Library", "Framework", "Language", "IDE"],
    //             "correct": "Language"
    //         },
    //         {
    //             "question": "What is MongoDB?",
    //             "options": ["Library", "Framework", "Language", "Database"],
    //             "correct": "Database"
    //         }
    //     ]
    // }

    useEffect(() => {
        fetch(`${config.server}/CreateMCQ?` + new URLSearchParams({
            query: params.Question
        }))
            .then(r => r.json())
            .then(d => {
                console.log(d)
                setMCQ(d)
            })
    }, [])
    const checkQuestion = () => {
        if (currentQuestion === (mcq.question.length - 1)) {
            setGameOver(true)
        }
        if (selectedOption === mcq.question[currentQuestion].correct) {
            setCurrentResult(1)
            increasePlayerScore(1)
            setTimeout(() => {
                setCurrentResult(null)
            }, 1000)
        } else {
            decreasePlayerLives()
            setCurrentResult(0)
        }
        setGoNext(true)
    }
    const goNext = () => {
        currentQuestion < (mcq.question.length - 1) ? setCurrentQuestion(currentQuestion + 1) : setCompleted(true)
        setGoNext(false)
        setCurrentResult(null)
    }
    if (playerLives === 0) {
        return <div className="p-6 bg-orange-400 h-screen flex  flex-col justify-between">
            <div>
                <h1 className="text-3xl font-black">Better Luck Next Time {session.data?.user?.name?.split(' ')[0]} 😔</h1>
                <h1 className=" text-3xl font-bold mt-2">
                    You Lost All you Hearts
                </h1>

            </div>
            <Button onClick={() => router.push('/')} className="w-full h-16 text-lg font-bold mb-4">
                Continue
            </Button>

        </div>
    }

    if (gameOver) {
        return <div className="p-6 bg-orange-400 h-screen flex  flex-col justify-between">
            <div>
                <h1 className="text-3xl font-black">Amazing Work {session.data?.user?.name?.split(' ')[0]} !</h1>
                <h1 className=" text-3xl font-bold mt-1">
                    You Scored
                </h1>
                <h1 className={`${rbk.className
                    } text-9xl font-black`}>{playerScore}</h1>
            </div>
            <Button onClick={() => router.push('/')} className="w-full h-16 text-lg font-bold mb-4">
                Continue
            </Button>

        </div>
    }

    if (mcq === null) {
        return <>Loading..</>
    }
    return <div className="">
        <div className="px-8 pt-6 flex items-center  justify-between gap-2  ">
            <Confetti
                className="fixed w-full h-full "
                width={width}
                height={height}
                numberOfPieces={currentResult === 1 ? 100 : 0}
            />
            <button onClick={() => router.back()} className=" text-xl  p-1.5  hover:bg-white/10 rounded-full">
                <MaterialSymbolsArrowBackRounded />
            </button>
            <div className="w-full h-8 bg-neutral-950 rounded-full p-0.5 ">
                <div style={{ width: `${((currentQuestion + 1) / mcq.question.length) * 100}%` }} className="h-full transition-all  duration-700  ease-in-out bg-orange-400 rounded-full pt-1.5 px-4">
                    <div className="w-full h-1 bg-white/20 rounded-full" />
                </div>
            </div>
            <div className="h-8 w-40  rounded-full relative flex">
                <MaterialSymbolsFavoriteRounded className={`text-3xl ${playerLives >= 1 ? "text-rose-600" : "text-neutral-300/10"}`} />
                <MaterialSymbolsFavoriteRounded className={`text-3xl ${playerLives >= 2 ? "text-rose-600" : "text-neutral-300/10"}`} />
                <MaterialSymbolsFavoriteRounded className={`text-3xl ${playerLives >= 3 ? "text-rose-600" : "text-neutral-300/10"}`} />
                <MaterialSymbolsFavoriteRounded className={`text-3xl ${playerLives >= 4 ? "text-rose-600" : "text-neutral-300/10"}`} />
                <MaterialSymbolsFavoriteRounded className={`text-3xl ${playerLives >= 5 ? "text-rose-600" : "text-neutral-300/10"}`} />
            </div>
        </div>

        <div className="p-8">
            <h1 className="text-2xl font-black">{mcq.question[currentQuestion].question}</h1>
        </div>
        <div className="grid grid-cols-2 gap-2  px-8">
            {mcq.question[currentQuestion].options.split(",").map((option, i) => <><Button disabled={goNextState} onClick={() => option !== selectedOption ? setSelectedOption(option) : setSelectedOption(null)} className={`${selectedOption === option ? "border-b-4 border-l-4 bg-orange-300" : "hover:bg-orange-300  hover:border-b-4 hover:border-l-4 bg-orange-400"} ${(selectedOption === option) && (currentResult === 0) ? "bg-red-500 border-red-700" : "border-orange-500 "} h-16  active:bg-orange-300   rounded-bl-xl   relative`}>
                {option}
            </Button>
            </>)}
        </div>
        <div className={`${selectedOption !== null ? "" : "translate-y-24"} transition-transform fixed bottom-0 w-full p-3 bg-orange-800 shadow-lg rounded-t-lg space-y-2`}>

            <Button onClick={goNextState ? goNext : checkQuestion} className="w-full h-14 rounded-lg">{goNextState ? "Next" : "Submit"}</Button>
            {/* <Button disabled={!goNextState} onClick={goNext} className="w-full h-14 rounded-lg">Next</Button> */}
        </div>

    </div>
}
