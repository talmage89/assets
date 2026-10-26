"""Assembly ownership and small manufacturing details for the Field 3 family."""
import bpy
from kit import model as G,materials as M


class Build:
    def __init__(self,high,wear,marks):
        self.high=high;self.wear=wear;self.edges=3 if high else 1
        self.circle=64 if high else 24
        self.root=G.pivot('Grill',(0,0,0));self.root['static_root']=True
        self.materials={key:M.surface('M_'+key,key,wear) for key in M.FINISHES}
        m=self.materials
        m['tire']=M.surface('M_scuffed_tire','rubber',wear,wheel_radius=(.073,.089),dust=.9)
        m['brass']=M.surface('M_valve_brass','brass',wear,color=(.32,.22,.09),roughness=.47,grime=.6,dust=.05)
        m['powder']=M.surface('M_contact_worn_frame','powder',wear,dust=.35,grime=.25,chip_height=(.15,.02),
                zones=[dict(center=(x,z),radii=(.028,.048)) for x in (-.296,.296) for z in (.055,.315,.72)])
        m['casting']=M.surface('M_coated_casting','powder',wear,color=(.014,.016,.014),dust=.18,roughness=.59,grime=.8,deposits=[dict(x=x,z=.89,width=w,length=.14,direction=(0,-1,0)) for x,w in [(-.19,.007),(.07,.005),(.24,.004)]])
        m['inside']=M.combustion('M_seasoned_hood_carbon',wear,'hood')
        m['bowl']=M.combustion('M_grease_carbon_bowl',wear,'bowl')
        m['grate']=M.surface('M_satin_black_porcelain_iron','cast_iron',wear,grime=.8,heat=.6,heat_height=(.878,.015),cook_zones=[dict(center=(x,y),radii=(.095,.13),axes=(0,1)) for x,y in [(-.17,-.06),(.14,.045),(.04,-.10)]])
        m['tent']=M.combustion('M_flame_carbon_heat_channels',wear,'channel')
        m['burner']=M.ported_burner('M_ported_heat_tinted_burners',wear)
        m['shelf']=M.surface('M_settled_cart_dust','powder',wear,dust=.95,grime=.12)
        m['stainless_used']=M.surface('M_brushed_worktops','stainless',wear,dust=.12,heat=.35,heat_height=(.867,.018),heat_zones=[dict(center=(x,.03),radii=(.050,.25),axes=(0,1)) for x in (-.34,.34)],
                zones=[dict(center=(-.47,.03),radii=(.08,.10),axes=(0,1)),dict(center=(.51,-.10),radii=(.07,.05),axes=(0,1))])
        m['enamel']=M.surface('M_porcelain_hood','enamel',wear,grime=.7,heat=.12,heat_height=(.205,.015),
                zones=[dict(center=(-.225,.070),radii=(.043,.038)),dict(center=(.225,.070),radii=(.043,.038))])
        m['handle']=M.surface('M_hand_scuffed_grip','plastic',wear,color=(.012,.014,.012),grime=.5,zones=[dict(center=(x,.056),radii=(.075,.022)) for x in (-.13,.13)])
        m['lip']=M.surface('M_greasy_front_lip','powder',wear,color=(.012,.014,.012),grime=2.3,
                deposits=[(-.23,.90,.008,.055),(-.08,.90,.013,.04),(.13,.90,.009,.06),(.255,.90,.006,.035)])
        m['tray']=M.surface('M_grease_tray_stainless','stainless',wear,grime=2.3,heat=.5,heat_height=(.033,.04),
                deposits=[(-.083,.025,.009,.075),(.032,.025,.007,.07),(.113,.025,.005,.08)],roughness=.52)
        m['zinc']=M.surface('M_pressed_zinc_regulator','cast_aluminum',wear,color=(.12,.13,.13),roughness=.38,grime=.9,dust=.12)
        m['red']=M.surface('M_pointer_red','plastic',wear,color=(.37,.018,.009),roughness=.55)
        fascia=M.surface('M_handled_fascia','stainless',wear,grime=.55,
                zones=[dict(center=(-.205,.012),radii=(.043,.04)),dict(center=(0,-.01),radii=(.04,.03)),
                       dict(center=(.205,.012),radii=(.04,.04))],roughness=.39)
        void=M.Nodes('M_deep_aperture');m['void']=void.finish((.0002,.0002,.0002),1,0)
        m['void'].node_tree.nodes['SURFACE'].inputs['Specular IOR Level'].default_value=0
        m['panel_print']=M.print_material('M_fascia_ink',marks/'panel.png',fascia)
        m['badge_print']=M.print_material('M_enameled_maker_badge',marks/'badge.png')
        m['dial_print']=M.print_material('M_thermometer_dial',marks/'gauge.png')
        m['scale_print']=M.print_material('M_spring_scale_graphics',marks/'scale.png')
    def mat(self,key):return self.materials[key] if isinstance(key,str) else key
    def add(self,ob,parent=None,aset='Grill'):
        return G.attach(ob,parent or self.root,aset)
    def box(self,name,center,size,material='powder',radius=.001,parent=None,aset='Grill'):
        if not self.high and (min(size)<.006 or max(size)<.035):radius=0
        return self.add(G.box(name,center,size,self.mat(material),radius,self.edges),parent,aset)
    def cylinder(self,name,a,b,radius,material='stainless',segments=None,parent=None,aset='Grill'):
        return self.add(G.cylinder(name,a,b,radius,self.mat(material),segments or (24 if self.high else 12)),parent,aset)
    def fastener(self,name,position,direction=(0,-1,0),radius=.0045,kind='hex',parent=None,aset='Grill',washer=True):
        for part in G.fastener(name,position,direction,self.mat('stainless'),radius,self.high,kind,washer):
            self.add(part,parent,aset)
    def weld(self,name,points,radius=.001,parent=None,aset='Grill',material='powder'):
        if self.high:self.add(G.weld(name,points,radius,self.mat(material),True),parent,aset)
    def tube(self,name,points,radius,material='stainless',sides=None,parent=None,aset='Grill'):
        return self.add(G.tube(name,points,radius,self.mat(material),sides or (12 if self.high else 6)),parent,aset)
    def lathe(self,name,profile,material,segments=None,axis='Z',center=(0,0),closed=False,parent=None,aset='Grill'):
        return self.add(G.lathe(name,profile,self.mat(material),segments or self.circle,axis,center,closed),parent,aset)
    def profile(self,name,points,lo,hi,material='powder',axis='X',radius=.001,parent=None,aset='Grill'):
        if not self.high and radius<.0015:radius=0
        return self.add(G.profile(name,points,lo,hi,self.mat(material),axis,radius,self.edges),parent,aset)
