import { useState } from 'react'
import { Button } from "/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "/components/ui/card"
import { Input } from "/components/ui/input"
import { Label } from "/components/ui/label"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "/components/ui/table"
import { Textarea } from "/components/ui/textarea"
import { Home, Calendar, Vote, MessageSquare, Shield } from "lucide-react"

type Officer = {
  id: number
  name: string
  rank: string
  beat: string
  duty: string
  monthlyPercentage: number
  yearlyPercentage: number
}

type Duty = {
  id: number
  officerId: number
  beat: string
  date: string
  shift: string
}

type ChatMessage = {
  id: number
  officerId: number
  message: string
  photoUrl?: string
  timestamp: string
}

type Vote = {
  id: number
  officerId: number
  rating: number
  date: string
}

export default function OfficerManagement() {
  // Authentication state
  const [isAdmin, setIsAdmin] = useState(false)
  const [isOfficer, setIsOfficer] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  
  // Navigation state
  const [activeTab, setActiveTab] = useState('home')
  
  // Data state
  const [officers, setOfficers] = useState<Officer[]>([
    { id: 1, name: 'John Doe', rank: 'Sergeant', beat: 'Beat 1', duty: 'Day Shift', monthlyPercentage: 85, yearlyPercentage: 78 },
    { id: 2, name: 'Jane Smith', rank: 'Officer', beat: 'Beat 2', duty: 'Night Shift', monthlyPercentage: 92, yearlyPercentage: 88 },
    { id: 3, name: 'Mike Johnson', rank: 'Lieutenant', beat: 'Beat 3', duty: 'Day Shift', monthlyPercentage: 78, yearlyPercentage: 82 },
  ])
  
  const [duties, setDuties] = useState<Duty[]>([
    { id: 1, officerId: 1, beat: 'Beat 1', date: '2023-06-01', shift: 'Morning' },
    { id: 2, officerId: 2, beat: 'Beat 2', date: '2023-06-01', shift: 'Night' },
    { id: 3, officerId: 3, beat: 'Beat 3', date: '2023-06-01', shift: 'Morning' },
  ])
  
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    { id: 1, officerId: 1, message: 'Completed patrol without incidents', timestamp: '2023-06-01 08:30' },
    { id: 2, officerId: 2, message: 'Reported suspicious activity', timestamp: '2023-06-01 22:15' },
  ])
  
  const [votes, setVotes] = useState<Vote[]>([
    { id: 1, officerId: 1, rating: 4, date: '2023-06-01' },
    { id: 2, officerId: 2, rating: 5, date: '2023-06-01' },
  ])
  
  const [newOfficer, setNewOfficer] = useState<Omit<Officer, 'id'>>({
    name: '',
    rank: '',
    beat: '',
    duty: '',
    monthlyPercentage: 0,
    yearlyPercentage: 0
  })
  
  const [newMessage, setNewMessage] = useState('')
  const [newVote, setNewVote] = useState<{officerId: number, rating: number}>({officerId: 1, rating: 3})

  // Authentication handlers
  const handleAdminLogin = () => {
    if (username === 'admin' && password === 'admin') {
      setIsAdmin(true)
    }
  }

  const handleOfficerLogin = () => {
    if (username) {
      setIsOfficer(true)
    }
  }

  const handleLogout = () => {
    setIsAdmin(false)
    setIsOfficer(false)
    setUsername('')
    setPassword('')
  }

  // Data handlers
  const addOfficer = () => {
    const newId = officers.length > 0 ? Math.max(...officers.map(o => o.id)) + 1 : 1
    setOfficers([...officers, { ...newOfficer, id: newId }])
    setNewOfficer({
      name: '',
      rank: '',
      beat: '',
      duty: '',
      monthlyPercentage: 0,
      yearlyPercentage: 0
    })
  }

  const removeOfficer = (id: number) => {
    setOfficers(officers.filter(officer => officer.id !== id))
  }

  const addDuty = (beat: string) => {
    const newId = duties.length > 0 ? Math.max(...duties.map(d => d.id)) + 1 : 1
    setDuties([...duties, { 
      id: newId, 
      officerId: 1, // Default to first officer for demo
      beat, 
      date: new Date().toISOString().split('T')[0], 
      shift: 'Morning' 
    }])
  }

  const removeDuty = (id: number) => {
    setDuties(duties.filter(duty => duty.id !== id))
  }

  const addChatMessage = () => {
    if (!newMessage.trim()) return
    
    const newId = chatMessages.length > 0 ? Math.max(...chatMessages.map(m => m.id)) + 1 : 1
    setChatMessages([...chatMessages, { 
      id: newId, 
      officerId: 1, // Default to first officer for demo
      message: newMessage, 
      timestamp: new Date().toLocaleString() 
    }])
    setNewMessage('')
  }

  const addVote = () => {
    const newId = votes.length > 0 ? Math.max(...votes.map(v => v.id)) + 1 : 1
    setVotes([...votes, { 
      id: newId, 
      officerId: newVote.officerId, 
      rating: newVote.rating, 
      date: new Date().toISOString().split('T')[0] 
    }])
  }

  // Render login screen if not authenticated
  if (!isAdmin && !isOfficer) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-2xl font-bold">Officer Management System</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username"
                />
              </div>
              <div>
                <Label htmlFor="password">Password (Admin only)</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password"
                />
              </div>
              <div className="flex space-x-2">
                <Button onClick={handleAdminLogin} className="w-full">
                  Admin Login
                </Button>
                <Button onClick={handleOfficerLogin} className="w-full" variant="outline">
                  Officer Login
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Main application layout
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Officer Management System</h1>
          <Button onClick={handleLogout} variant="outline">
            Logout
          </Button>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex space-x-8">
              <button
                onClick={() => setActiveTab('home')}
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'home' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >
                <Home className="mr-2 h-4 w-4" />
                Home
              </button>
              <button
                onClick={() => setActiveTab('duty')}
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'duty' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >
                <Calendar className="mr-2 h-4 w-4" />
                Duty Schedule
              </button>
              <button
                onClick={() => setActiveTab('voting')}
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'voting' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >
                <Vote className="mr-2 h-4 w-4" />
                Voting
              </button>
              <button
                onClick={() => setActiveTab('chat')}
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'chat' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >
                <MessageSquare className="mr-2 h-4 w-4" />
                Chat Box
              </button>
              <button
                onClick={() => setActiveTab('patrol')}
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'patrol' ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >
                <Shield className="mr-2 h-4 w-4" />
                Patrol Duties
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Home Tab */}
        {activeTab === 'home' && (
          <Card>
            <CardHeader>
              <CardTitle>Officer Management</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Rank</TableHead>
                    <TableHead>Beat</TableHead>
                    <TableHead>Duty</TableHead>
                    <TableHead>Monthly %</TableHead>
                    <TableHead>Yearly %</TableHead>
                    {isAdmin && <TableHead>Actions</TableHead>}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {officers.map((officer) => (
                    <TableRow key={officer.id}>
                      <TableCell>{officer.name}</TableCell>
                      <TableCell>{officer.rank}</TableCell>
                      <TableCell>{officer.beat}</TableCell>
                      <TableCell>{officer.duty}</TableCell>
                      <TableCell>{officer.monthlyPercentage}%</TableCell>
                      <TableCell>{officer.yearlyPercentage}%</TableCell>
                      {isAdmin && (
                        <TableCell>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => removeOfficer(officer.id)}
                          >
                            Remove
                          </Button>
                        </TableCell>
                      )}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {isAdmin && (
                <div className="mt-6 space-y-4">
                  <h3 className="text-lg font-medium">Add New Officer</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name">Name</Label>
                      <Input
                        id="name"
                        value={newOfficer.name}
                        onChange={(e) => setNewOfficer({ ...newOfficer, name: e.target.value })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="rank">Rank</Label>
                      <Input
                        id="rank"
                        value={newOfficer.rank}
                        onChange={(e) => setNewOfficer({ ...newOfficer, rank: e.target.value })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="beat">Beat</Label>
                      <Input
                        id="beat"
                        value={newOfficer.beat}
                        onChange={(e) => setNewOfficer({ ...newOfficer, beat: e.target.value })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="duty">Duty</Label>
                      <Input
                        id="duty"
                        value={newOfficer.duty}
                        onChange={(e) => setNewOfficer({ ...newOfficer, duty: e.target.value })}
                      />
                    </div>
                  </div>
                  <Button onClick={addOfficer}>Add Officer</Button>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Duty Schedule Tab */}
        {activeTab === 'duty' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Duty Schedule - Beat 1</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Shift</TableHead>
                      {isAdmin && <TableHead>Actions</TableHead>}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {duties.filter(d => d.beat === 'Beat 1').map((duty) => (
                      <TableRow key={duty.id}>
                        <TableCell>{officers.find(o => o.id === duty.officerId)?.name || 'Unknown'}</TableCell>
                        <TableCell>{duty.date}</TableCell>
                        <TableCell>{duty.shift}</TableCell>
                        {isAdmin && (
                          <TableCell>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDuty(duty.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                {isAdmin && (
                  <div className="mt-4">
                    <Button onClick={() => addDuty('Beat 1')}>Add Duty</Button>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Duty Schedule - Beat 2</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Shift</TableHead>
                      {isAdmin && <TableHead>Actions</TableHead>}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {duties.filter(d => d.beat === 'Beat 2').map((duty) => (
                      <TableRow key={duty.id}>
                        <TableCell>{officers.find(o => o.id === duty.officerId)?.name || 'Unknown'}</TableCell>
                        <TableCell>{duty.date}</TableCell>
                        <TableCell>{duty.shift}</TableCell>
                        {isAdmin && (
                          <TableCell>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDuty(duty.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                {isAdmin && (
                  <div className="mt-4">
                    <Button onClick={() => addDuty('Beat 2')}>Add Duty</Button>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Duty Schedule - Beat 3</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Shift</TableHead>
                      {isAdmin && <TableHead>Actions</TableHead>}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {duties.filter(d => d.beat === 'Beat 3').map((duty) => (
                      <TableRow key={duty.id}>
                        <TableCell>{officers.find(o => o.id === duty.officerId)?.name || 'Unknown'}</TableCell>
                        <TableCell>{duty.date}</TableCell>
                        <TableCell>{duty.shift}</TableCell>
                        {isAdmin && (
                          <TableCell>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDuty(duty.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                {isAdmin && (
                  <div className="mt-4">
                    <Button onClick={() => addDuty('Beat 3')}>Add Duty</Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Voting Tab */}
        {activeTab === 'voting' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Vote Officers</CardTitle>
                <CardDescription>Rate officers from 1 to 5 stars</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="officer">Officer</Label>
                    <select
                      id="officer"
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      value={newVote.officerId}
                      onChange={(e) => setNewVote({...newVote, officerId: parseInt(e.target.value)})}
                    >
                      {officers.map(officer => (
                        <option key={officer.id} value={officer.id}>{officer.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <Label htmlFor="rating">Rating</Label>
                    <select
                      id="rating"
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      value={newVote.rating}
                      onChange={(e) => setNewVote({...newVote, rating: parseInt(e.target.value)})}
                    >
                      {[1, 2, 3, 4, 5].map(rating => (
                        <option key={rating} value={rating}>{rating} star{rating !== 1 ? 's' : ''}</option>
                      ))}
                    </select>
                  </div>
                  <Button onClick={addVote}>Submit Vote</Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Voting Results</CardTitle>
                <CardDescription>Performance metrics based on votes</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Average Rating</TableHead>
                      <TableHead>Total Votes</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {officers.map(officer => {
                      const officerVotes = votes.filter(v => v.officerId === officer.id)
                      const averageRating = officerVotes.length > 0 
                        ? (officerVotes.reduce((sum, vote) => sum + vote.rating, 0) / officerVotes.length).toFixed(1)
                        : 'No votes'
                      return (
                        <TableRow key={officer.id}>
                          <TableCell>{officer.name}</TableCell>
                          <TableCell>{averageRating}</TableCell>
                          <TableCell>{officerVotes.length}</TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
                <div className="mt-4">
                  <Button variant="outline">Download PDF Report</Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Chat Box Tab */}
        {activeTab === 'chat' && (
          <Card>
            <CardHeader>
              <CardTitle>Chat Box</CardTitle>
              <CardDescription>Upload photos and remarks about duty schedules</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="border rounded-lg p-4 h-64 overflow-y-auto">
                  {chatMessages.map(message => (
                    <div key={message.id} className="mb-4">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold">
                          {officers.find(o => o.id === message.officerId)?.name || 'Unknown'}
                        </span>
                        <span className="text-sm text-gray-500">{message.timestamp}</span>
                      </div>
                      <p className="mt-1">{message.message}</p>
                      {message.photoUrl && (
                        <div className="mt-2">
                          <div className="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16" />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="message">New Message</Label>
                  <Textarea
                    id="message"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Enter your message..."
                  />
                </div>
                <div className="flex justify-between">
                  <Button variant="outline">
                    Upload Photo
                  </Button>
                  <Button onClick={addChatMessage}>Send Message</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Patrol Duties Tab */}
        {activeTab === 'patrol' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Patrol Duties - Beat 1</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Shift</TableHead>
                      {isAdmin && <TableHead>Actions</TableHead>}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {duties.filter(d => d.beat === 'Beat 1').map((duty) => (
                      <TableRow key={duty.id}>
                        <TableCell>{officers.find(o => o.id === duty.officerId)?.name || 'Unknown'}</TableCell>
                        <TableCell>{duty.date}</TableCell>
                        <TableCell>{duty.shift}</TableCell>
                        {isAdmin && (
                          <TableCell>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDuty(duty.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                {isAdmin && (
                  <div className="mt-4">
                    <Button onClick={() => addDuty('Beat 1')}>Add Patrol</Button>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Patrol Duties - Beat 2</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Shift</TableHead>
                      {isAdmin && <TableHead>Actions</TableHead>}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {duties.filter(d => d.beat === 'Beat 2').map((duty) => (
                      <TableRow key={duty.id}>
                        <TableCell>{officers.find(o => o.id === duty.officerId)?.name || 'Unknown'}</TableCell>
                        <TableCell>{duty.date}</TableCell>
                        <TableCell>{duty.shift}</TableCell>
                        {isAdmin && (
                          <TableCell>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDuty(duty.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                {isAdmin && (
                  <div className="mt-4">
                    <Button onClick={() => addDuty('Beat 2')}>Add Patrol</Button>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Patrol Duties - Beat 3</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Officer</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Shift</TableHead>
                      {isAdmin && <TableHead>Actions</TableHead>}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {duties.filter(d => d.beat === 'Beat 3').map((duty) => (
                      <TableRow key={duty.id}>
                        <TableCell>{officers.find(o => o.id === duty.officerId)?.name || 'Unknown'}</TableCell>
                        <TableCell>{duty.date}</TableCell>
                        <TableCell>{duty.shift}</TableCell>
                        {isAdmin && (
                          <TableCell>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeDuty(duty.id)}
                            >
                              Remove
                            </Button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                {isAdmin && (
                  <div className="mt-4">
                    <Button onClick={() => addDuty('Beat 3')}>Add Patrol</Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  )
}
