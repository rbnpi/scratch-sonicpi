#Sonic Pi Scratch3 interface by Robin Newman, May 2020
#two programs. Uncomment one section OR the other at a time
#first section sets Sonic PI as a keyboard instrument with dsaw synth
#second section has selectors to play sample groups, chords and two sample sub programs
use_osc "localhost",8000
#osc "/testprint","hello there"
osc "/start",0
set :flag,true
define :groove1 do
  live_loop :g1 do
    synth :tb303,note: scale(:c3,:minor_pentatonic,num_octaves: 3).choose,release: 0.2,cutoff: rrand_i(60,110)
    sleep 0.2
    stop if get(:kill)
  end
end


define :groove2 do
  l1=(ring 1,0,1,0,1,0,1,0,1,0,1,0)
  l2=(ring 0,1,0,1,0,1,0,1,0,1,0,1)
  l3=(ring 0,1,0,0,1,1,0,1,0,1,0,1)
  l4=(ring 1,0,1,0,1,1,0,1,0,1,0,1)
  l=(ring l1,l2,l3,l4)
  
  live_loop :drums1 do
    r=l.tick(:l)
    24.times do
      stop if get(:kill2) #check for when to stop this thread
      tick
      a=0.5;a=1 if look%3==0
      sample :drum_tom_hi_hard,amp: a,pan: [-1,1].choose  if r.look==1
      sleep 0.1
    end
  end
  
  live_loop :drums2 do
    stop if get(:kill2) #check for when to stop this thread
    a=0.5;a=1 if tick%4==0
    sample :drum_tom_lo_hard,amp: a,pan: [-0.5,0.5].choose
    sleep 0.3
  end
end

live_loop :waitReset do
  use_real_time
  r = sync "/osc*/reset"
  set :flag,false
  osc "/start",1
end

with_fx :reverb,room: 0.8,mix: 0.7 do
  uncomment do #uncomment for dsaw synth player
    use_synth :dsaw
    
    live_loop :test do
      use_real_time
      k = sync "/osc*/playOn"
      if get(:flag) == true
        puts k[0]
        z= play 60+k[0],sustain: 5
        k=sync "/osc*/playOff"
        control z,amp: 0,amp_slide: 0.05
        sleep 0.05
        kill z
      else
        stop
      end
    end
  end
  
  comment do #uncomment for sample /chords/live_loop player
    live_loop :test2 do
      use_real_time
      k= sync "/osc*/playOn"
      if get(:flag) == true
        p=k[0]
        puts p
        case p
        when 0
          z=sample (sample_names sample_groups[0]).choose
        when 1
          z=sample (sample_names sample_groups[1]).choose
        when 2
          z=sample (sample_names sample_groups[2]).choose
        when 3
          z=sample (sample_names sample_groups[3]).choose
        when 4
          z=sample (sample_names sample_groups[4]).choose
        when 5
          z=sample (sample_names sample_groups[5]).choose
        when 6
          z=sample (sample_names sample_groups[6]).choose
        when 7
          z=sample (sample_names sample_groups[7]).choose
        when 8
          z=sample (sample_names sample_groups[8]).choose
        when 9
          z=sample (sample_names sample_groups[9]).choose
        when 10
          z=sample (sample_names sample_groups[10]).choose
          
        when 11
          z=sample (sample_names sample_groups[11]).choose
        when 12
          z=sample (sample_names sample_groups[12]).choose
        when 13
          z=sample (sample_names sample_groups[13]).choose
        when 14
          z = synth :tb303,note: chord_degree([1,3,5,8].choose,:c3,:major,3),sustain: 5,cutoff: rrand_i(80,100)
        when 15
          z = synth :fm,note: chord_degree([1,3,5,8].choose,:c4,:major,3),sustain: 5,cutoff: rrand_i(80,100)
        when 16
          z = synth :zawa,note: chord_degree([1,3,5,8].choose,:c3,:major,3),sustain: 5,cutoff: rrand_i(80,100)
        when 17
          z = synth :mod_saw,note: chord_degree([1,3,5,8].choose,:c3,:major,3),sustain: 5,cutoff: rrand_i(80,100)
        when 18
          set :kill,false #flag used for killing groove1
          groove1
        when 19
          set :kill2,false #flag ued for killinggroove2
          groove2
        else
          puts p
        end
        k=sync "/osc*/playOff"
        if k[0]<18 #keys that handle stamples
          control z,amp: 0,amp_slide: 0.05
          sleep 0.05
          kill z #kill smple after quick fade
        end
        if k[0]==18 #keys that start live loop functions
          set :kill,true #kill groove1
        end
        if k[0]==19 #keys that start live loop functions
          set :kill2,true #kill groove2
        end
      end
    end
  end
end



