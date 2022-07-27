from geom import geom
from vector import vector

from schedule_funcs import schedule_funcs

schedule_tasks=schedule_funcs.schedule_tasks
task_class=schedule_funcs.task_class
convert_to_external=schedule_funcs.convert_to_external

def build_table(events,fn="test_calendar",vertical=True):
    
    #events=[(0,9,11,"hello there"),(2,17,18,"tea")]
    #I could use some calendar negotiation, but that's probably
    #more advanced and would fit better somewhere else.
    
    #let's just build a grid?
    out_o=[]
    d=0
    m=7
    
    x_size=0.6
    y_size=0.4
    if not vertical:
        x_size,y_size=y_size,x_size
        
    hour_spacing=0.6
    event_spacing=0
    day_spacing=x_size+0.3#hour_spacing
    
    offset=vector.Vector(0.05,0.05,0)
    text_off=vector.Vector(0,0.1,0)
    
    while d < m:
        h=0
        hm=24
        # ok so the hour looping is wrong,
        # i need to loop over the events
        # and draw from there.
        
        #wait this is drawing the grid.
        while h<hm:
            
            #flip direction
            if vertical:
                position=vector.Vector(d*day_spacing,h*hour_spacing,0)
            else:
                #let's go down for days.
                position=vector.Vector((h)*hour_spacing,-d*day_spacing,0)
                
            if d==0:
                if vertical:
                    this_v=vector.Vector(0.5,0,0)
                else:
                    this_v=vector.Vector(0.5-hour_spacing,-day_spacing,0)
                out_o.append(geom.Text(local_position=position-this_v,text=str(h)))
                
                
            out_o.append(geom.rectangle(d_vec=vector.Vector(x_size,y_size,0),
                local_position=position))
            
            h+=1
        
        h=0
        for event in events:
            if d==event[0]:
                h=event[1]
                duration=event[2]-event[1]-1
                
                if h+duration<24:
                    #if it fits on the table
                    if vertical:
                        position=vector.Vector(d*day_spacing,h*hour_spacing,0)
                    else:
                        position=vector.Vector(h*hour_spacing,-d*day_spacing,0)
                    tp=position.copy()
                    tp.x+=x_size*0.5
                    
                    if vertical:
                        d_vec=vector.Vector(x_size+0.1,y_size+0.1+hour_spacing*duration,0)
                        
                    else:
                        d_vec=vector.Vector(x_size+0.1+hour_spacing*duration,y_size+0.1,0)
                        
                    rec=geom.rectangle(local_position=position-offset,d_vec=d_vec)
                    out_o.append(rec)
                    
                    this_pos=rec.center
                    this_pos+=text_off
                    text_off= -text_off
                    
                    out_o.append(geom.Text(local_position=this_pos,text=event[3].name))
                    
                else:
                    this_day=23-h
                    overlap=(h+duration)-23
                    
                    #same day
                    if vertical:
                        position=vector.Vector(d*day_spacing,h*hour_spacing,0)
                    else:
                        position=vector.Vector(h*hour_spacing,-d*day_spacing,0)
                    tp=position.copy()
                    tp.x+=x_size*0.5
                    if vertical:
                        d_vec=vector.Vector(x_size+0.1,y_size+0.1+hour_spacing*this_day,0)
                        
                    else:
                        d_vec=vector.Vector(x_size+0.1+hour_spacing*this_day,y_size+0.1,0)
                    rec=geom.rectangle(local_position=position-offset, d_vec=d_vec)
                    out_o.append(rec)
                    this_pos=rec.center
                    this_pos+=text_off
                    text_off= - text_off
                    
                    out_o.append(geom.Text(local_position=this_pos,text=event[3].name))
                    
                    if True:
                        #next day
                        if d+1<7:
                            if vertical:
                                position=vector.Vector((d+1)*day_spacing,0,0)
                            else:
                                position=vector.Vector(0,-(d+1)*day_spacing,0)
                        else:
                            #loop around the week
                            if vertical:
                                position=vector.Vector((0)*day_spacing,0,0)
                            else:
                                position=vector.Vector(0,-(0)*day_spacing,0)
                            
                        tp=position.copy()
                        tp.x+=x_size*0.5
                        
                        if vertical:
                            d_vec=vector.Vector(x_size+0.1,y_size+0.1+hour_spacing*overlap,0)
                        
                        else:
                            d_vec=vector.Vector(x_size+0.1+hour_spacing*overlap,y_size+0.1,0)
                        rec=geom.rectangle(local_position=position-offset,d_vec=d_vec)
                        out_o.append(rec)
                        
                        this_pos=rec.center
                        this_pos+=text_off
                        text_off= - text_off
                        
                        #print("scheduling",event[3].name,"at",d,h)
                        out_o.append(geom.Text(local_position=this_pos,text=event[3].name[:6]))
                        
                    
        d+=1
    view_box_d=geom.make_view_box_d(out_o,scale=1.1)
    final_l=[]
    for x in out_o:
        final_l.append(x.as_svg())
        
        
    geom.main_svg(final_l,fn+".svg",view_box_d=view_box_d)
    
   
def test(vertical=True):
    tasks=[
            task_class("Task 1",0.5,4,priority=2),
            task_class("wake up",1,0,priority=0),
            task_class("work session",3,prefered_time=9,prefered_day_type="work",priority=0),
            task_class("work session2",5,prefered_time=14,prefered_day_type="work",priority=0),
            task_class("Task 2",1,prefered_day_frequency=1,priority=2),
            task_class("lunch break",2,prefered_time=12,priority=1),
            task_class("sleep",9,prefered_time=22,prefered_day_frequency=0,priority=0),
            ]
    schedule=schedule_tasks(tasks)
    build_table(schedule,"regular",vertical=vertical)
    
    schedule=convert_to_external(schedule)
    build_table(schedule,"blocked",vertical=vertical)

if __name__=="__main__":
    test()
    
