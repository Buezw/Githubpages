---
title: "MCMS 5. Further On Stress Strain"
date: 2024-10-16
tags: ["ECMS","Chemistry","Docs"]
series: ["ECMS"]
series_order: 5
math: mathjax


---
> Last Edit: 10/16/24


## Stress-Strain Curve
![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain.png) 

- 当回头重新看Stress-Strain Curve的时候可以发现一些特殊的点
- 如Proportion Limit，Ultimate Tensile Strength两个点

### Proportional Limit

- 在曲线的最初阶段，存在一个接近于Linear的区域，其代表了Linear Elastic的Region
- 而也必会存在一个点象征着Linear Elastic Region的结束
- 但犹豫一些测量的误差或者精度上的问题，将导致最终的这一个Linear Elastic结束的点无法被确定，所以需要一个约定俗成的方法

### 0.2% Offset Yield Strength

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-1.png) 

- 在\\(\epsilon=0.002\\)的位置画一个平行于Linear Elastic Region的直线，其交于SS Curve的位置即为Yield Strength

### ex. 
A hypothetical metal has a 0.2% offset yield strength of 358 MPa, an ultimate tensile strength of 522 MPa, and a fracture strength of 460 MPa.  A sample of this metal, originally 1 m in length with a cross section of 2 mm × 2 mm is loaded along its long axis. Just before fracture, while the load is still applied, the length is 1.3 m and when the load is released, the length is 1.18 m. Calculate the modulus of elasticity in GPa.（这我做集贸啊）

- 之前有公式\\(\sigma=E\epsilon\\)
- 现在需要将其推广到\\(E=\frac{\Delta \sigma}{\epsilon}\\)上
- \\(\Delta \sigma\\)：有460MPa-0MPa=460MPa
- \\(\epsilon\\)：有0.3-0.18=0.12

## Uniform deformation

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-2.png) 

- 在经历了Linear Elastic Region后，出现的便是Uniform Platic区间
- 这个阶段内，材料的塑性变形均匀地分布在整个试样或构件中

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-3.png) 

- 其具体的Unifrom体现在了变形过程中结构的完整性上
- 在Non-Unifrom Region中，材料已经发生了局部的Fracture，即产生了Neck
- 这也解释了为什么在过了Ultimate Tensile strength后Stress开始下降，即当金属样品承受的应力值逐渐增大时，最终会开始失效。 在拉伸过程中，当金属原子间的一些键断裂时，就会出现这种情况

## The Dislocation

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-4.png) 

- Disloaction广泛存在于各种晶体材料中，不仅限于金属。
- 它们在不同类型材料中的运动机制和对材料性能的影响各不相同。
- 例如，在金属中位错运动相对容易，而在陶瓷和半导体中则较为困难，且其作用更为复杂
- 具体来说存在有4种不同的Imperfections，来自不同的维度

### Dislocation Density

- Dislocation Density: 材料中单位体积内存在的位错数量
- Dislocation Density越高，材料的强度和硬度可能会有所增加，但延展性会降低

### Metal

- Dislocations are always present in metals. 
- 可以通过加热的方式更改Metal的dislocation density

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-6.png) 
![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-5.png) 

## Zero-Dimensional Imperfections or Point Defects

- 点缺陷（Point Defect）是指材料的晶体结构中，由于原子或离子位置上的异常，导致的局部晶体结构缺陷

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-7.png) 
### Interstitial Impurities

- Interstitial Impurities指的是一些较小的Atom（比如碳、氮等）进入了Crystal中本来空着的间隙位置

### Substitutional Impurities

- 当一个外来原子取代了晶体中正常位置上的原子时，形成Substitutional Impurities。
- 这种缺陷在合金中常见，例如铜和锌形成的黄铜

### Vacancies

- 在晶体中，一个本应有原子的位置上缺少了一个原子
- 它会导致周围的原子重新调整位置，影响材料的物理性质
- 但Vacancies的产生并不会导致Material的Strength发生改变s

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-9.png) 
### Zero-Dimension's Influence on Higher Dimension

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-8.png) 

- 当Zero Dimension Impurity发生的时候，其会对周围的Crystal Structure产生一个Strain Fields
- 这个Strain Field将会Repel其他的Atom进入Dislocation
- 其通常会造成一种One-Dimensional Imperfection

###  Ratio of the Number of Vacancies

$$\frac{N_v}{N} = e^{\frac{-Q_v}{kT}} \tag{1}$$

- **Nv​**：这是Crystal中**Number of Vancancies**，即晶体结构中缺失原子的位置数。
- **N**：Number of Atoms
- **Qv​**：表示生成一个Vacancies所需的**Energy**，通常以电子伏特（eV）为单位。
- **k**：这是**Boltzmann Constant**，数值约为 \\(1.38\times 10^{-23}J/K\\)，用于将温度与能量联系起来。
- **T**：这是**Thermodynamic temperature**，以开尔文（K）为单位，是热力学温度是根据热力学原理来衡量系统绝对温度的一个度量，其零点对应理论上的**绝对零度**，即系统的分子运动几乎完全停止、能量达到最低的状态。

- 从本质上讲，原子在它们的晶格位点上拼命振动，试图跳出它们的位点。 它们真的很努力。 我的意思是说，每秒大约有 1013 次！ 在固态中，由于结合能强于热能，大多数情况下它们都不会成功（实际上，原子形成有序固体有很大的节能作用，但我们稍后会详细介绍）。 但偶尔也会有原子从其晶格位置成功跃迁，并移动到晶格的其他位置。 这就会留下一个缺失的原子或空位。 因此，我们可以将空位的形成看作是将原子固定在晶格位点上的结合能与将原子从晶格位点上挤出的热能之间的持续斗争

### Thermodynamics 热力学

- Thermodynamics说明了在一个物体中，能量是分布在Atoms上而不是对于所有Atom都具有相同能量的

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-10.png) 

- 因此，单个原子可能有足够的能量跳出其晶格位置，而其余大多数原子则没有，这是有道理的

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-11.png) 

- 如图 10 所示，随着温度的升高，我们发现有更多的原子进入了高能态。 同时，随着温度的降低，高能态原子的数量也在减少。

### Boltzmann Distribution

- **在绝对零度（0 K）**：所有原子都会处于最低能量状态，因为此时系统没有足够的能量让原子占据更高的能量状态。
- **在无限温度（∞ K）**：系统的温度极高，粒子的能量足以占据任何能量状态。因此所有能量状态的粒子数都会趋于相等，也就是所有能量状态均等分布
- 在Boltzmann Distribution中，**不会出现所有粒子只占据最高能量状态**的情况，即使是在极高温度下

### One-Dimensional Imperfections or Dislocations

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-12.png) 
### Cold Work

- 当我们对金属进行Plastic Deformation时，会产生新的Dislocation。 这增加了Dislocation Density，这将在未来中增加Dislocation的难度
- 当我们观察金属的Stress-Strain Curve，发现应力在Yield Strength之后继续增加时，我们首次观察到金属通过Plastic Deformation而得到强化。 事实上，如果我们Unload一个sample并重新load，其在stress水平达到我们在前一个循环中留下的Stress之前不会开始Plastic Deformation
- 这是一种通过塑性变形进行的强化，不过在工业上，我们通常是通过轧制或拉动金属零件，或将金属零件压入模具来实现塑性变形，而不是通过简单的拉伸来拉动零件
## Hot Work

- 材料被加热到再结晶温度以上，这意味着减少了Dislocation Density

## Two-Dimensional Imperfections

### Free Surfaces

- **自由表面（Free Surfaces）** 是指材料的**外部表面**, 这些表面与外界环境直接接触
- **原子排列不规则**：在材料的自由表面，原子周围的配位数（与其他原子结合的数量）比材料内部的原子要少

### Grain Boundaries

- 是指多晶材料中不同Crystal Structure交界的地方

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-13.png) 

- 当Dislocation在Crystal中移动，其必定要穿过Grain Boundary，然而这对位错来说是一个挑战

![](/docs/EMCS_Static/ECMS5.FurtherOnStressStrain/MCMS5.FurtherOnStressStrain-14.png) 

- 如果我们减小金属的晶粒尺寸，就会产生更多的晶界和更多的位错运动障碍，从而有望提高金属的强度
- This strengthening mechanism has a pretty self-explanatory name: _grain size reduction_.

## Three-Dimensional Imperfections or Second Phase Particles

- Three-dimensional imperfections occur any time we have a second phase within a solid
- 从本质上讲，如果固体中存在晶体结构不同的区域，就会出现第二相或三维缺陷



























